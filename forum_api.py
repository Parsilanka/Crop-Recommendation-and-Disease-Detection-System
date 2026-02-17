"""
Forum API Endpoints
Handles all forum-related operations
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from community_models import db, ForumPost, ForumComment, ForumCategory, PostVote, CommentVote, PostFlag, User
from datetime import datetime
import bleach

forum_bp = Blueprint('forum', __name__, url_prefix='/api/forum')

# Allowed HTML tags for sanitization
ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'a', 'code', 'pre']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}


@forum_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all forum categories"""
    categories = ForumCategory.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'icon': cat.icon,
        'slug': cat.slug,
        'post_count': cat.post_count
    } for cat in categories])


@forum_bp.route('/posts', methods=['GET'])
def get_posts():
    """Get forum posts with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 20)
    category_id = request.args.get('category_id', type=int)
    location = request.args.get('location')
    sort_by = request.args.get('sort', 'newest')  # newest, trending, most_voted
    
    query = ForumPost.query
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    if location:
        query = query.filter_by(location=location)
    
    # Apply sorting
    if sort_by == 'newest':
        query = query.order_by(ForumPost.created_at.desc())
    elif sort_by == 'trending':
        query = query.order_by(ForumPost.views.desc(), ForumPost.created_at.desc())
    elif sort_by == 'most_voted':
        # This is simplified; in production, use a computed column
        query = query.order_by(ForumPost.created_at.desc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    posts = []
    for post in pagination.items:
        posts.append({
            'id': post.id,
            'title': post.title,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'author': {
                'id': post.author.id,
                'username': post.author.username,
                'reputation': post.author.reputation_points
            },
            'category': {
                'id': post.category.id,
                'name': post.category.name,
                'icon': post.category.icon
            },
            'location': post.location,
            'tags': post.tags.split(',') if post.tags else [],
            'vote_count': post.vote_count,
            'comment_count': post.comment_count,
            'views': post.views,
            'is_solved': post.is_solved,
            'is_pinned': post.is_pinned,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat()
        })
    
    return jsonify({
        'posts': posts,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@forum_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get single post with comments"""
    post = ForumPost.query.get_or_404(post_id)
    
    # Increment view count
    post.views += 1
    db.session.commit()
    
    # Get comments
    comments = []
    for comment in post.comments.filter_by(parent_comment_id=None).order_by(ForumComment.created_at.asc()):
        comments.append(format_comment(comment))
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'reputation': post.author.reputation_points,
            'is_expert': post.author.is_expert
        },
        'category': {
            'id': post.category.id,
            'name': post.category.name,
            'icon': post.category.icon
        },
        'location': post.location,
        'tags': post.tags.split(',') if post.tags else [],
        'image_url': post.image_url,
        'vote_count': post.vote_count,
        'comment_count': post.comment_count,
        'views': post.views,
        'is_solved': post.is_solved,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'comments': comments
    })


def format_comment(comment):
    """Format comment with nested replies"""
    return {
        'id': comment.id,
        'content': comment.content,
        'author': {
            'id': comment.author.id,
            'username': comment.author.username,
            'reputation': comment.author.reputation_points,
            'is_expert': comment.author.is_expert
        },
        'vote_count': comment.vote_count,
        'is_best_answer': comment.is_best_answer,
        'created_at': comment.created_at.isoformat(),
        'replies': [format_comment(reply) for reply in comment.replies.order_by(ForumComment.created_at.asc())]
    }


@forum_bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    """Create new forum post"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('title') or not data.get('content') or not data.get('category_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Sanitize content
    clean_content = bleach.clean(data['content'], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    
    post = ForumPost(
        title=data['title'],
        content=clean_content,
        author_id=current_user.id,
        category_id=data['category_id'],
        location=data.get('location', current_user.location),
        tags=data.get('tags', ''),
        image_url=data.get('image_url')
    )
    
    db.session.add(post)
    
    # Update category post count
    category = ForumCategory.query.get(data['category_id'])
    if category:
        category.post_count += 1
    
    # Add reputation points
    current_user.add_reputation(
        current_app.config.get('POINTS_POST_CREATED', 5),
        'post_created',
        post.id
    )
    
    db.session.commit()
    
    return jsonify({'id': post.id, 'message': 'Post created successfully'}), 201


@forum_bp.route('/posts/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    """Update post (author only)"""
    post = ForumPost.query.get_or_404(post_id)
    
    if post.author_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = bleach.clean(data['content'], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    if 'tags' in data:
        post.tags = data['tags']
    
    post.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Post updated successfully'})


@forum_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    """Delete post (author or admin only)"""
    post = ForumPost.query.get_or_404(post_id)
    
    if post.author_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Update category post count
    if post.category:
        post.category.post_count = max(0, post.category.post_count - 1)
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted successfully'})


@forum_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add comment to post"""
    post = ForumPost.query.get_or_404(post_id)
    data = request.get_json()
    
    if not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    clean_content = bleach.clean(data['content'], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    
    comment = ForumComment(
        content=clean_content,
        post_id=post_id,
        author_id=current_user.id,
        parent_comment_id=data.get('parent_comment_id')
    )
    
    db.session.add(comment)
    
    # Add reputation points
    current_user.add_reputation(
        current_app.config.get('POINTS_COMMENT_CREATED', 2),
        'comment_created',
        comment.id
    )
    
    db.session.commit()
    
    return jsonify({'id': comment.id, 'message': 'Comment added successfully'}), 201


@forum_bp.route('/posts/<int:post_id>/vote', methods=['POST'])
@login_required
def vote_post(post_id):
    """Vote on a post"""
    post = ForumPost.query.get_or_404(post_id)
    data = request.get_json()
    vote_type = data.get('vote_type')  # 'upvote' or 'downvote'
    
    if vote_type not in ['upvote', 'downvote']:
        return jsonify({'error': 'Invalid vote type'}), 400
    
    # Check if user already voted
    existing_vote = PostVote.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote
            db.session.delete(existing_vote)
            message = 'Vote removed'
        else:
            # Change vote
            existing_vote.vote_type = vote_type
            message = 'Vote updated'
    else:
        # New vote
        vote = PostVote(post_id=post_id, user_id=current_user.id, vote_type=vote_type)
        db.session.add(vote)
        message = 'Vote recorded'
        
        # Add reputation to post author
        if vote_type == 'upvote':
            post.author.add_reputation(
                current_app.config.get('POINTS_UPVOTE_RECEIVED', 10),
                'upvote_received',
                post.id
            )
    
    db.session.commit()
    
    return jsonify({'message': message, 'vote_count': post.vote_count})


@forum_bp.route('/comments/<int:comment_id>/vote', methods=['POST'])
@login_required
def vote_comment(comment_id):
    """Vote on a comment"""
    comment = ForumComment.query.get_or_404(comment_id)
    data = request.get_json()
    vote_type = data.get('vote_type')
    
    if vote_type not in ['upvote', 'downvote']:
        return jsonify({'error': 'Invalid vote type'}), 400
    
    existing_vote = CommentVote.query.filter_by(comment_id=comment_id, user_id=current_user.id).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            db.session.delete(existing_vote)
            message = 'Vote removed'
        else:
            existing_vote.vote_type = vote_type
            message = 'Vote updated'
    else:
        vote = CommentVote(comment_id=comment_id, user_id=current_user.id, vote_type=vote_type)
        db.session.add(vote)
        message = 'Vote recorded'
        
        if vote_type == 'upvote':
            comment.author.add_reputation(5, 'comment_upvote_received', comment.id)
    
    db.session.commit()
    
    return jsonify({'message': message, 'vote_count': comment.vote_count})


@forum_bp.route('/search', methods=['GET'])
def search_posts():
    """Search forum posts"""
    query_text = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 20)
    
    if not query_text:
        return jsonify({'posts': [], 'pagination': {}})
    
    # Simple search (in production, use full-text search)
    query = ForumPost.query.filter(
        db.or_(
            ForumPost.title.contains(query_text),
            ForumPost.content.contains(query_text),
            ForumPost.tags.contains(query_text)
        )
    ).order_by(ForumPost.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    posts = [{
        'id': post.id,
        'title': post.title,
        'content': post.content[:200] + '...',
        'author': {'username': post.author.username},
        'category': {'name': post.category.name, 'icon': post.category.icon},
        'created_at': post.created_at.isoformat()
    } for post in pagination.items]
    
    return jsonify({
        'posts': posts,
        'pagination': {
            'page': page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })


@forum_bp.route('/posts/<int:post_id>/flag', methods=['POST'])
@login_required
def flag_post(post_id):
    """Flag post for moderation"""
    post = ForumPost.query.get_or_404(post_id)
    data = request.get_json()
    
    if not data.get('reason'):
        return jsonify({'error': 'Reason is required'}), 400
    
    flag = PostFlag(
        post_id=post_id,
        user_id=current_user.id,
        reason=data['reason']
    )
    
    db.session.add(flag)
    db.session.commit()
    
    return jsonify({'message': 'Post flagged for review'}), 201

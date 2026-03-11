from fpdf import FPDF
import os


class ResearchProposal(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toc_data = []

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_to_toc(self, title, level=0):
        self.toc_data.append({'title': title, 'page': self.page_no(), 'level': level})

    def chapter_heading(self, text):
        self.add_to_toc(text, level=0)
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 0, 0)
        self.ln(10)
        self.cell(0, 10, text, 0, 1, 'C')
        self.ln(5)

    def section_title(self, text):
        self.add_to_toc(text, level=1)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.ln(6)
        self.cell(0, 8, text, 0, 1, 'L')
        self.ln(2)

    def sub_section_title(self, text):
        self.add_to_toc(text, level=2)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(0, 0, 0)
        self.ln(4)
        self.cell(0, 7, text, 0, 1, 'L')
        self.ln(2)

    def body(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text, align='J')
        self.ln(3)

    def roman_item(self, num, text):
        self.set_font('Helvetica', '', 11)
        y = self.get_y()
        self.set_xy(20, y)
        self.cell(12, 6, f'{num}.', 0, 0)
        self.set_xy(32, y)
        self.multi_cell(158, 6, text, align='J')
        self.ln(1)

    def bold_label(self, label, text):
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 7, label, 0, 1)
        self.set_font('Helvetica', '', 11)
        self.set_left_margin(20)
        self.multi_cell(0, 6, text, align='J')
        self.set_left_margin(15)
        self.ln(2)

    def req_item(self, req_id, text):
        self.set_font('Helvetica', '', 11)
        y = self.get_y()
        self.set_xy(20, y)
        self.cell(15, 6, req_id, 0, 0)
        self.set_xy(35, y)
        self.multi_cell(155, 6, text, align='J')
        self.ln(1)

    def draw_toc(self, entries):
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, 'TABLE OF CONTENTS', 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(0, 0, 0)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(4)

        for e in entries:
            title = e['title']
            page = e['page']
            level = e['level']
            indent = level * 8
            self.set_x(15 + indent)

            if level == 0:
                self.set_font('Helvetica', 'B', 11)
            elif level == 1:
                self.set_font('Helvetica', '', 11)
            else:
                self.set_font('Helvetica', '', 10)

            tw = self.get_string_width(title)
            self.cell(tw + 2, 7, title, 0, 0, 'L')
            cx = self.get_x()
            tx = 183
            dw = self.get_string_width('.')
            if dw > 0 and tx > cx:
                nd = int((tx - cx) / dw)
                self.set_text_color(150, 150, 150)
                self.cell(tx - cx, 7, '.' * nd, 0, 0, 'L')
                self.set_text_color(0, 0, 0)
            self.cell(12, 7, str(page), 0, 1, 'R')
            self.ln(1)


def build_document(pdf, show_toc=False, toc_entries=None):
    pdf.set_margins(15, 20, 15)
    pdf.set_auto_page_break(True, margin=20)

    students = [
        ('CT203/113825/23', 'FAITH CHEPKORIR'),
        ('CT203/113823/23', 'SAMUEL LEMAIYAN'),
        ('CT203/113803/23', 'CLARENCE YAA'),
        ('CT203/113827/23', 'DAISY CHELANGAT'),
        ('CT203/113837/23', 'KINDNESS EBENEZER'),
        ('CT203/109347/22', 'ALFRED MUSYOKI'),
        ('CT203/113799/23', 'SCHOLAR WAMBOI'),
    ]

    # ============================================================
    # PAGE 1: COVER PAGE
    # ============================================================
    pdf.add_page()

    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'must_logo.png')
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=87, y=20, w=32)
        pdf.ln(42)
    else:
        pdf.ln(10)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, 'MERU UNIVERSITY OF SCIENCE AND TECHNOLOGY', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'SCHOOL OF COMPUTING AND INFORMATICS', 0, 1, 'C')
    pdf.cell(0, 7, 'DEPARTMENT OF INFORMATION TECHNOLOGY', 0, 1, 'C')
    pdf.ln(14)

    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.6)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(10)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.multi_cell(0, 8,
        'AN INTELLIGENT CROP RECOMMENDATION AND PLANT DISEASE\n'
        'DETECTION SYSTEM FOR ENHANCED AGRICULTURAL\n'
        'DECISION-MAKING',
        0, 'C')
    pdf.ln(8)
    pdf.set_line_width(0.6)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(10)

    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 7, 'BY', 0, 1, 'C')
    pdf.ln(4)

    # Students -- reg number left, name right, entire block centered
    pdf.set_font('Helvetica', '', 11)
    col_reg_w = 52
    col_name_w = 55
    block_w = col_reg_w + 8 + col_name_w
    left_x = (210 - block_w) / 2
    for reg, name in students:
        pdf.set_x(left_x)
        pdf.cell(col_reg_w, 7, reg, 0, 0, 'L')
        pdf.cell(8, 7, '', 0, 0)
        pdf.cell(col_name_w, 7, name, 0, 1, 'L')

    # Add spacing then submission block below the student list naturally
    pdf.ln(12)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6,
        'A RESEARCH PROPOSAL SUBMITTED TO THE DEPARTMENT OF INFORMATION TECHNOLOGY\n'
        'IN THE SCHOOL OF COMPUTING AND INFORMATICS IN PARTIAL FULFILLMENT\n'
        'OF RESEARCH METHODOLOGY AND GROUP PROJECT UNIT WORK\n'
        'OF MERU UNIVERSITY OF SCIENCE AND TECHNOLOGY',
        0, 'C')
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'SUPERVISOR:', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'Mwendwa Gichuru', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'FEBRUARY 2026', 0, 1, 'C')

    # ============================================================
    # PAGE 2: DECLARATION
    # ============================================================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 10, 'DECLARATION', 0, 1, 'C')
    pdf.ln(5)

    pdf.body(
        'We, the undersigned, declare that this research proposal is our original work and has not been '
        'presented for a degree or any other academic award in any university or institution of higher '
        'learning. Where other peoples work has been used, it has been duly acknowledged.'
    )
    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "Students' Declaration", 0, 1, 'L')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(65, 8, 'Name', 1, 0, 'C', fill=True)
    pdf.cell(65, 8, 'Registration No.', 1, 0, 'C', fill=True)
    pdf.cell(50, 8, 'Signature & Date', 1, 1, 'C', fill=True)
    pdf.set_font('Helvetica', '', 10)
    for reg, name in students:
        pdf.cell(65, 9, name.title(), 1, 0, 'L')
        pdf.cell(65, 9, reg, 1, 0, 'C')
        pdf.cell(50, 9, '', 1, 1, 'C')
    pdf.ln(12)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, "Supervisor's Declaration", 0, 1, 'L')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6,
        'This research proposal has been submitted for examination with my approval as the university supervisor.')
    pdf.ln(8)
    pdf.cell(100, 7, 'Name: Mwendwa Gichuru', 0, 0)
    pdf.cell(0, 7, 'Signature: ____________________', 0, 1)
    pdf.ln(5)
    pdf.cell(0, 7, 'Date: ____________________', 0, 1)

    # ============================================================
    # PAGE 3: TABLE OF CONTENTS
    # ============================================================
    pdf.add_page()
    if show_toc and toc_entries:
        pdf.draw_toc(toc_entries)
    else:
        pdf.set_font('Helvetica', 'I', 10)
        pdf.cell(0, 10, '(Table of Contents placeholder)', 0, 1, 'C')

    # ============================================================
    # CHAPTER 1: INTRODUCTION
    # ============================================================
    pdf.add_page()
    pdf.chapter_heading('CHAPTER ONE: INTRODUCTION')

    pdf.section_title('1.1 Background of the Study')
    pdf.body(
        'Agriculture forms the backbone of many developing economies, providing food security, '
        'employment, and raw materials for industry. The rapid advancement of computing technologies has '
        'permeated virtually every sector of the economy, including agriculture (Liakos et al., 2018). The '
        'integration of Artificial Intelligence (AI) and Machine Learning (ML) into agricultural practices has '
        'opened new frontiers for precision farming, enabling farmers to make data-driven decisions that '
        'optimize crop yields and reduce losses.'
    )
    pdf.body(
        'Crop recommendation systems leverage soil properties and environmental parameters to guide '
        'farmers on which crops to cultivate in a particular region. Traditional approaches relied heavily on '
        'the subjective judgment of agricultural extension officers, which was often inaccessible to '
        'smallholder farmers in rural areas (Mucherino et al., 2009). With the proliferation of affordable '
        'smartphones and internet connectivity, web-based systems now offer a scalable alternative that can '
        'reach millions of farmers simultaneously.'
    )
    pdf.body(
        'Plant disease is a major threat to food production worldwide, causing losses estimated at 10-16% of '
        'global crop yields annually (Strange & Scott, 2005). Early and accurate detection of plant diseases '
        'is critical to effective management and the reduction of pesticide overuse. Historically, disease '
        'diagnosis depended on visual inspection by skilled agronomists, a process that is both '
        'time-consuming and expensive, and often unavailable to resource-limited farmers (Mohanty et al., 2016).'
    )
    pdf.body(
        'The advent of deep learning, particularly Convolutional Neural Networks (CNNs), has revolutionized '
        'image-based plant disease detection. Mohanty et al. (2016) demonstrated that CNN models trained '
        'on the PlantVillage dataset could achieve over 99% accuracy in identifying 26 crop diseases across '
        '14 plant species in controlled conditions. Subsequent research has extended these capabilities to '
        'real-world field applications, though challenges such as varying lighting conditions and image quality '
        'remain (Ferentinos, 2018).'
    )
    pdf.body(
        'Web-based agricultural advisory systems integrate these ML capabilities into accessible platforms. '
        'Such systems typically combine crop recommendation modules, disease detection, fertilizer '
        'advisory, and weather integration to provide holistic decision support (Kamilaris & Prenafeta-Boldu, '
        '2018). The present study aims to develop and evaluate such an integrated system, tailored to the '
        'needs of Kenyan smallholder farmers, by combining a Random Forest-based crop recommendation '
        'engine with a CNN-based plant disease detection module within a secure, user-authenticated web '
        'application.'
    )

    pdf.section_title('1.2 Problem Statement')
    pdf.body(
        'Modern agricultural practice demands timely, accurate, and accessible advisory services that can '
        'guide farmers in selecting the most suitable crops and identifying plant diseases at the earliest stage '
        'possible. Ideally, a farmer should be able to input soil and environmental parameters and receive an '
        'evidence-based crop recommendation, upload a plant leaf photograph and receive an instant '
        'disease diagnosis with actionable treatment advice, and review historical records of their analyses '
        'through a personal secure account.'
    )
    pdf.body(
        'However, the current reality for most smallholder farmers in Kenya is markedly different. Agricultural '
        'advisory services are largely manual, dependent on the physical availability of extension officers, '
        'and prone to human error and subjectivity. Farmers lack access to integrated digital tools that '
        'simultaneously address crop selection, disease diagnosis, and fertilizer guidance. Existing solutions '
        'are fragmented, with separate, unconnected tools for each function, creating inefficiencies and '
        'barriers to adoption. Furthermore, most available systems do not provide personalized accounts, '
        'preventing farmers from tracking their historical decisions and progress over time.'
    )
    pdf.body(
        'The consequences of this gap are severe: suboptimal crop selection leads to reduced yields and '
        'economic losses; delayed disease identification results in uncontrolled outbreaks; and the absence '
        'of integrated reporting means that farmers cannot monitor trends or demonstrate compliance for '
        'agricultural financing. This study therefore proposes the development of an integrated, web-based '
        'intelligent system that combines user authentication, ML-driven crop recommendation, CNN-based '
        'disease detection, and automated report generation to address these critical gaps.'
    )

    pdf.section_title('1.3 Research Objectives')
    pdf.body(
        'The purpose of this research project is to develop an intelligent, web-based Crop Recommendation '
        'and Plant Disease Detection System that should be able to:'
    )
    pdf.roman_item('i', 'To develop a farmer registration system.')
    pdf.roman_item('ii', 'To develop a crop recommendation module based on soil, environmental parameters.')
    pdf.roman_item('iii', 'To develop a plant disease detection module using uploaded leaf images.')
    pdf.roman_item('iv', 'To provide disease management advice.')
    pdf.roman_item('v', 'To generate downloadable PDF reports.')

    pdf.section_title('1.4 Research Questions')
    pdf.roman_item('i', 'How will the system allow users to register?')
    pdf.roman_item('ii', 'How will the system recommend crops based on soil, environmental parameters?')
    pdf.roman_item('iii', 'How will the system detect plant diseases from uploaded leaf images?')
    pdf.roman_item('iv', 'How will the system provide disease management advice?')
    pdf.roman_item('v', 'How will the system generate downloadable reports?')

    pdf.section_title('1.5 Significance of the Study')
    pdf.body(
        'This research makes a significant contribution to the intersection of artificial intelligence and '
        'agricultural development. At a societal level, the system will contribute directly to food security by '
        'enabling farmers to maximize yields through evidence-based crop selection and timely disease '
        'intervention, thereby reducing crop losses and improving livelihoods for smallholder farmers in '
        'Kenya and similar developing-world contexts.'
    )
    pdf.body(
        'For farmers, the system will provide a free, accessible, and easy-to-use digital advisory tool that '
        'eliminates the dependency on scarce agricultural extension officers. It will empower farmers with '
        'knowledge previously accessible only to well-funded large-scale agricultural enterprises. The user '
        'authentication and history tracking module will allow farmers to maintain records of their analyses, '
        'which can be used to demonstrate adoption of best practices to agricultural financing institutions.'
    )
    pdf.body(
        "For agricultural researchers and policymakers, the system's data collection capabilities provide an "
        'opportunity to aggregate crop health and disease prevalence data across regions, informing '
        'national agricultural planning and early-warning systems for disease outbreaks. The report '
        'generation feature ensures that users and institutions can extract structured information for further '
        'analysis and decision-making.'
    )
    pdf.body(
        'From an academic standpoint, this project advances research in the application of Random Forest '
        'classifiers and Convolutional Neural Networks to agricultural problems, contributes a documented, '
        'tested integrated system to the body of knowledge, and provides a reproducible framework that '
        'future researchers can build upon.'
    )

    pdf.section_title('1.6 Scope of the Study')
    pdf.body(
        'This research project will focus on the design, development, and evaluation of a web-based '
        'integrated agricultural advisory system. The scope is defined as follows:'
    )

    pdf.sub_section_title('1.6.1 Crop Types')
    pdf.body(
        'The system will support crop recommendation for 22 major crops represented in the Crop '
        'Recommendation dataset (including rice, maize, wheat, chickpea, cotton, coffee, and others). '
        'Disease detection will cover 38 plant disease classes spanning 14 plant species as defined by the '
        'PlantVillage dataset.'
    )

    pdf.sub_section_title('1.6.2 User Management')
    pdf.body(
        'The system will include user registration and login functionality with secure password hashing. '
        'Users will have personal dashboards to view their analysis history.'
    )

    pdf.sub_section_title('1.6.3 Crop Recommendation')
    pdf.body(
        'Recommendations will be generated based on six input parameters: Nitrogen (N), Phosphorus (P), '
        'Potassium (K), pH, temperature, humidity, and rainfall. The model will use a trained Random Forest classifier.'
    )

    pdf.sub_section_title('1.6.4 Disease Detection')
    pdf.body(
        'Disease detection will be performed on uploaded leaf images (PNG/JPG/JPEG format, maximum 16 MB) '
        'using a pre-trained CNN model. When the CNN model is unavailable, a color-pattern-based '
        'fallback classifier will be used.'
    )

    pdf.sub_section_title('1.6.5 Report Generation')
    pdf.body(
        'The system will generate downloadable PDF reports for both crop recommendation and disease '
        'detection analyses, summarizing inputs, results, confidence levels, treatment advice, and fertilizer recommendations.'
    )

    pdf.sub_section_title('1.6.6 Geographic Focus')
    pdf.body(
        'The system is primarily targeted at farmers in Kenya, though its functionality is applicable to any '
        'agriculture region with similar crop types.'
    )

    pdf.sub_section_title('1.6.7 Platform')
    pdf.body(
        'The system will be delivered as a Flask web application accessible via a standard web browser. '
        'Mobile responsiveness will be implemented for smartphone accessibility. The project will be '
        'completed by the end of the academic semester, April 2026.'
    )

    # ============================================================
    # CHAPTER 2: LITERATURE REVIEW
    # ============================================================
    pdf.add_page()
    pdf.chapter_heading('CHAPTER TWO: LITERATURE REVIEW')

    pdf.body(
        'This chapter presents a review of literature relevant to the development of an intelligent, web-based '
        'Crop Recommendation and Plant Disease Detection System. The review adopts an integrative '
        'approach, critiquing and synthesizing secondary data from existing studies, systems, and '
        'frameworks to generate new perspectives on the subject. The integrative literature review was '
        'selected because it allows the identification of gaps in existing knowledge and provides a foundation '
        'for proposing improvements. Unlike narrative reviews, which may lack systematic rigor, the '
        'integrative approach employed here combines insights from both quantitative and qualitative '
        'studies, drawing on peer-reviewed journals, conference papers, and technical reports published '
        'between 2005 and 2024.'
    )
    pdf.body(
        'Other types of literature review include systematic reviews, which require a rigidly defined search '
        'protocol and are typically used for clinical or policy questions; argumentative reviews, which '
        'selectively examine literature to support a specific position; and theoretical reviews, which map and '
        'critique existing theoretical frameworks. While elements of theoretical reasoning are incorporated in '
        'the discussion of machine learning models below, the dominant approach of this chapter remains integrative.'
    )

    pdf.section_title('2.1 Functions of Existing Intelligent Agricultural Advisory Systems')
    pdf.body(
        'Existing intelligent agricultural advisory systems perform a range of core functions that have evolved '
        'significantly with advances in computing and artificial intelligence. The primary function of such '
        'systems is decision support: providing farmers and agronomists with evidence-based guidance on '
        'crop selection, pest and disease management, irrigation scheduling, and fertilizer application (Liakos et al., 2018).'
    )
    pdf.body(
        'Crop recommendation is one of the most widely implemented functions. Systems such as those '
        'developed by Sharma et al. (2021) and Kumar et al. (2020) use soil nutrient data (Nitrogen, '
        'Phosphorus, and Potassium levels), pH values, and environmental parameters (temperature, '
        'humidity, and rainfall) to predict the most suitable crop for a given region. These systems function by '
        'training supervised machine learning classifiers on historical agronomic datasets, enabling real-time '
        'prediction through a web interface.'
    )
    pdf.body(
        'Disease detection and diagnosis constitutes the second major functional domain. Systems in this '
        'category accept image inputs of plant leaves and return a disease classification along with a '
        'confidence score (Mohanty et al., 2016). The most capable systems go beyond simple classification '
        'to provide treatment recommendations, management protocols, and, in some cases, the economic '
        'impact of the identified disease (Ferentinos, 2018). A third key function, which has become '
        'increasingly important, is personalized advisory delivery: matching recommendations to the specific '
        'context of the user, including geographic location, crop history, and soil type. User authentication '
        'and history management modules underpin this personalization capability, ensuring that each '
        "farmer's data is securely stored and retrievable for longitudinal monitoring (Kamilaris & Prenafeta-Boldu, 2018)."
    )

    pdf.section_title('2.2 Components of Existing Intelligent Agricultural Advisory Systems')
    pdf.body(
        'A typical intelligent agricultural advisory system comprises several interacting components. At the '
        'data layer, systems incorporate soil databases, meteorological data feeds, plant disease image '
        'repositories (such as the PlantVillage dataset), and user-contributed data. The PlantVillage dataset, '
        'which contains over 54,000 expertly curated images representing 38 disease classes across 14 '
        'plant species, has become the de facto benchmark for plant disease detection research (Hughes & Salathe, 2015).'
    )
    pdf.body(
        'At the processing layer, machine learning models perform classification tasks. Random Forest '
        'classifiers are widely used for crop recommendation due to their robustness to overfitting, ability to '
        'handle mixed data types, and interpretability (Mucherino et al., 2009). For disease detection, '
        'Convolutional Neural Networks (CNNs), particularly architectures such as VGG16, ResNet, and '
        'InceptionV3, have demonstrated superior performance in image classification tasks (Ferentinos, '
        '2018). Transfer learning, which involves fine-tuning pre-trained CNNs on domain-specific datasets, '
        'has significantly reduced the computational cost and data requirements of training accurate disease '
        'detection models (Kamilaris & Prenafeta-Boldu, 2018).'
    )
    pdf.body(
        'The presentation layer includes the user interface, which in web-based systems is typically rendered '
        'using HTML, CSS, and JavaScript frameworks. Backend components include API endpoints (often '
        'implemented in Python frameworks such as Flask or Django) that receive user inputs, invoke model '
        'inference, and return results. Auxiliary components include report generation modules, notification '
        'services, and integration with external data sources such as weather APIs.'
    )

    pdf.section_title('2.3 Characteristics and Features of Existing Systems')
    pdf.body(
        'Effective intelligent agricultural advisory systems share several defining characteristics. First, '
        'accuracy is paramount: systems must exhibit high classification accuracy across the crop types and '
        'disease classes they support. Mohanty et al. (2016) reported CNN accuracy of up to 99.35% on the '
        'PlantVillage test set under controlled conditions, although field performance is typically lower due to '
        'variability in image quality, lighting, and background clutter. Second, accessibility is critical for '
        'adoption by smallholder farmers, necessitating mobile-responsive interfaces, low bandwidth '
        'requirements, and support for local languages. Third, scalability is a key feature, as effective '
        'systems must handle growing user bases without degradation in performance. Cloud-based '
        'deployment using platforms such as AWS, Google Cloud, or Heroku has been widely adopted to address this requirement.'
    )
    pdf.body(
        'Fourth, security is increasingly important as systems collect and store sensitive agronomic and '
        'personal data. Secure password hashing, role-based access control, and encrypted data '
        'transmission are standard features in modern systems (Kamilaris & Prenafeta-Boldu, 2018). Fifth, '
        'interpretability of model outputs is important for farmer trust and adoption. Systems that accompany '
        'predictions with confidence scores, visual heatmaps, or natural-language explanations have been '
        'shown to improve user confidence and decision quality (Sharma et al., 2021).'
    )

    pdf.section_title('2.4 Types of Existing Intelligent Agricultural Advisory Systems')
    pdf.body(
        'Existing intelligent agricultural advisory systems can be broadly classified into four types based on '
        'their scope and primary function.'
    )

    pdf.sub_section_title('2.4.1 Standalone Crop Recommendation Systems')
    pdf.body(
        'These systems focus exclusively on recommending crops based on soil and climatic parameters. '
        'Kumar et al. (2020) developed a web-based crop recommendation system using a Naive Bayes '
        'classifier trained on soil pH, NPK levels, and weather data, achieving 90.6% accuracy. While '
        'effective for their intended purpose, such systems do not address disease detection or reporting, limiting their utility as comprehensive advisory tools.'
    )

    pdf.sub_section_title('2.4.2 Standalone Disease Detection Systems')
    pdf.body(
        'These systems focus on plant disease diagnosis from images. The work of Mohanty et al. (2016) '
        'established the feasibility of CNN-based plant disease detection. Subsequent systems by '
        'Ramcharan et al. (2017) demonstrated field-deployable disease detection for cassava using '
        'smartphones, achieving over 93% accuracy on six disease and pest categories. However, these '
        'systems lack crop recommendation and reporting capabilities.'
    )

    pdf.sub_section_title('2.4.3 Integrated Crop Management Systems')
    pdf.body(
        'A growing number of systems integrate multiple functions, including crop recommendation, disease '
        'detection, weather forecasting, and market price information. FarmHack and PlantNet are examples '
        'of community-driven platforms that aggregate diverse agricultural intelligence. However, most '
        'commercial platforms are proprietary, subscription-based, and designed for large-scale operations, '
        'placing them beyond the reach of smallholder farmers in developing economies.'
    )

    pdf.sub_section_title('2.4.4 Expert Knowledge Systems')
    pdf.body(
        'These systems encode agronomist expertise in rule-based engines. While they provide interpretable '
        'recommendations, they are costly to develop and maintain, and lack the adaptability of machine '
        'learning-based approaches. They have largely been superseded by ML-based systems in recent literature.'
    )

    pdf.section_title('2.5 Challenges of Existing Intelligent Agricultural Advisory Systems')

    pdf.sub_section_title('2.5.1 Data Quality and Availability')
    pdf.body(
        'Machine learning models are only as good as the data they are trained on. The PlantVillage dataset, '
        'while large, consists primarily of images captured under controlled, laboratory-like conditions. '
        'Ferentinos (2018) observed a significant drop in CNN model accuracy when evaluated on field '
        'images, highlighting the dataset distribution shift problem. Collecting sufficiently large, diverse, and '
        'annotated datasets for locally specific crops remains a major challenge, particularly in sub-Saharan '
        'Africa where many staple crops are underrepresented in global datasets.'
    )

    pdf.sub_section_title('2.5.2 Connectivity and Infrastructure Barriers')
    pdf.body(
        'Many agricultural regions in developing countries lack reliable internet connectivity. While '
        'offline-capable mobile applications have been proposed as a solution, they require local model '
        'deployment on resource-constrained devices, which introduces trade-offs between model '
        'complexity and inference speed (Kamilaris & Prenafeta-Boldu, 2018).'
    )

    pdf.sub_section_title('2.5.3 Model Explainability and Farmer Trust')
    pdf.body(
        'Black-box nature of deep learning models presents a trust barrier. Farmers are unlikely to follow '
        'advice they cannot understand or verify, particularly when the recommendation contradicts their '
        'traditional knowledge. The lack of transparent reasoning in CNN outputs remains an active area of '
        'research, with gradient-weighted class activation mapping (Grad-CAM) and Shapley values being '
        'proposed as partial solutions (Strange & Scott, 2005).'
    )

    pdf.sub_section_title('2.5.4 System Integration and Fragmentation')
    pdf.body(
        'As noted by Liakos et al. (2018), most existing systems address a single aspect of agricultural '
        'decision-making. The lack of integration between crop recommendation, disease detection, fertilizer '
        'advisory, and reporting creates inefficiencies and forces farmers and extension officers to use '
        'multiple disconnected tools.'
    )

    pdf.sub_section_title('2.5.5 Security and Data Privacy')
    pdf.body(
        'Agricultural data is commercially sensitive. Existing systems frequently lack robust authentication '
        'and data protection mechanisms, exposing farmers to data theft and misuse by agribusiness '
        'competitors. Few open-source agricultural advisory systems implement industry-standard security '
        'practices such as password hashing, HTTPS enforcement, and session management.'
    )

    pdf.section_title('2.6 Related Studies and Work')
    pdf.body(
        'Several studies are directly relevant to the proposed system and provide important insights for its design and implementation.'
    )
    pdf.body(
        'Mohanty et al. (2016) conducted a landmark study using a CNN trained on 54,306 images from the '
        'PlantVillage dataset to classify 26 diseases across 14 crop species. The model achieved 99.35% '
        'accuracy in a constrained, single-image classifier setting. While this study established the viability of '
        'deep learning for plant disease detection, it also acknowledged that real-field performance would be '
        'lower due to background noise and image quality variability. The proposed system draws on this '
        'methodology but incorporates a color-pattern-based fallback classifier to maintain functionality when '
        'a trained CNN model is unavailable, directly addressing the deployment gap identified by Mohanty et al.'
    )
    pdf.body(
        'Ferentinos (2018) trained and evaluated several CNN architectures on PlantVillage, finding that '
        'deeper networks (VGG, AlexNet) achieved higher accuracy but required substantially more '
        'computational resources. The study highlighted the trade-off between model complexity and '
        'deployability, a consideration that directly informed the architecture decisions of the proposed '
        'system, which prioritizes lightweight, deployable models over maximum theoretical accuracy.'
    )
    pdf.body(
        'Kumar et al. (2020) developed a crop recommendation system using several ML classifiers '
        '(Decision Tree, Random Forest, Naive Bayes, SVM, and Logistic Regression) trained on a dataset '
        'of 2,200 records covering 22 crop types. Random Forest achieved the highest accuracy of 99.09%, '
        'affirming its suitability for this task. The proposed system adopts the Random Forest classifier for '
        "crop recommendation, corroborated by this finding, while augmenting the output with fertilizer "
        "recommendations and weather-integrated advice not present in Kumar et al.'s system."
    )
    pdf.body(
        'Sharma et al. (2021) developed an integrated crop and disease advisory platform using a Flask '
        'backend and a CNN disease detection module. Their system demonstrated the feasibility of '
        'combining crop recommendation and disease detection in a single application. However, their '
        'system lacked user authentication, personalized history tracking, and PDF report generation, '
        'functionalities that are central to the proposed system. This gap reinforces the value of the '
        "proposed system's contribution."
    )
    pdf.body(
        'Ramcharan et al. (2017) optimized CNN models for field deployment on mobile devices for cassava '
        'disease detection, achieving high recall for economically significant diseases using data collected by '
        'Tanzanian farmers. Their work underscored the importance of training with locally representative '
        'images and the potential of smartphone-based advisory tools. The proposed system does not '
        'constrain itself to a single crop and provides a web-based interface accessible from any device with '
        "a browser, extending Ramcharan et al.'s scope."
    )
    pdf.body(
        'Kamilaris and Prenafeta-Boldu (2018) conducted a comprehensive survey of deep learning '
        'applications in agriculture, reviewing 40 studies across crop management, animal farming, water '
        'management, and soil management. They identified the lack of standardized benchmarks, '
        'cross-domain integration, and interpretability as the primary barriers to wider adoption. The '
        'proposed system addresses the integration barrier directly by combining crop recommendation, '
        'disease detection, fertilizer advisory, and report generation within a single authenticated platform.'
    )

    pdf.section_title('2.7 Summary')
    pdf.body(
        'The literature reviewed in this chapter reveals that significant progress has been made in the '
        'application of machine learning and deep learning to agricultural advisory systems. Random Forest '
        'classifiers have emerged as the most reliable approach for crop recommendation, while CNN-based '
        'models, trained on large image datasets such as PlantVillage, have demonstrated strong potential '
        'for plant disease detection. However, a critical gap persists: most existing systems are either siloed, '
        'addressing only one functional domain, or are designed for large-scale commercial agriculture, '
        'leaving the needs of smallholder farmers largely unmet.'
    )
    pdf.body(
        'Key shortcomings identified across the reviewed literature include: (i) lack of integration between '
        'crop recommendation, disease detection, and advisory functions; (ii) absence of user authentication '
        'and personalized history tracking; (iii) inadequate security measures for protecting farmer data; (iv) '
        'no provision for automated report generation; and (v) poor field-condition robustness due to training '
        'data limitations. The proposed system directly addresses each of these gaps by delivering a unified, '
        'authenticated, web-based platform with ML-driven crop recommendation, CNN-based disease '
        'detection, integrated treatment and fertilizer advice, and PDF report generation. The following '
        'chapter describes the research methodology that will guide the system\'s development and evaluation.'
    )

    # ============================================================
    # CHAPTER 3: METHODOLOGY
    # ============================================================
    pdf.add_page()
    pdf.chapter_heading('CHAPTER THREE: METHODOLOGY')

    pdf.section_title('3.0 Overview')
    pdf.body(
        'This chapter outlines the methodology adopted in the design and development of the Intelligent '
        'Crop Recommendation and Plant Disease Detection System. The key components are: research '
        'design, population and sampling, data collection methods, development tools and materials, '
        'system development methodology, system design, and data processing and analysis.'
    )

    pdf.section_title('3.1 Research Design')
    pdf.body(
        'A research design is the arrangement of conditions for collection and analysis of data in a manner '
        'that aims to combine relevance to the research purpose with economy in procedure. It constitutes '
        'the blueprint for the collection, measurement and analysis of data. As such the design includes an '
        'outline of what the researcher will do from writing the research objectives and its operational '
        'implications to the final analysis of data.'
    )
    pdf.body(
        'This study adopts an Experimental Research Design. Experimental design allows some cases to be '
        'exposed to all levels of the independent variable of interest. This design is appropriate for this '
        'project because the system must be constructed, deployed, and evaluated against measurable '
        'performance criteria such as crop recommendation accuracy, disease detection confidence, and '
        'user satisfaction scores. A quantitative approach is adopted to effectively show how the system '
        'improves agricultural decision-making among smallholder farmers.'
    )

    pdf.sub_section_title('3.1.1 Variables in the Study')
    pdf.body(
        'A concept which can take on different quantitative values is called a variable. The independent '
        'variables in this study include soil fertility parameters (Nitrogen, Phosphorus, Potassium, pH), '
        'environmental conditions (temperature, humidity, rainfall), and plant leaf image inputs provided by '
        'the user. The dependent variables are the accuracy of crop recommendations produced by the '
        'Random Forest model and the correctness of disease diagnosis produced by the CNN model. '
        'Extraneous variables such as camera quality, network connectivity, and ambient lighting during '
        'image capture will be controlled where possible.'
    )

    pdf.section_title('3.2 Population and Sampling')
    pdf.body(
        'Population is a well-defined collection of individuals or objects known to have similar '
        'characteristics. Sampling is a process of selecting a portion of objects or individuals from a group '
        'or population to become the foundation for estimating and predicting the outcome of the population.'
    )
    pdf.body(
        'The target population for this research comprises 2,500 smallholder farmers in Meru County, '
        'Kenya. The choice of this population was based on accessibility and relevance to the research '
        'context. Stratified sampling will be used to divide the population by primary farming activity, '
        'ensuring all categories are represented. The sample size is calculated using the Fisher et al. '
        '(1998) formula: n = Z2PQ/d2, giving a sample of approximately 346 respondents.'
    )

    pdf.set_font('Helvetica', 'B', 10)
    pdf.ln(5)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(60, 8, 'Stratum', 1, 0, 'C', fill=True)
    pdf.cell(60, 8, 'Population', 1, 0, 'C', fill=True)
    pdf.cell(60, 8, 'Sample Size', 1, 1, 'C', fill=True)
    pdf.set_font('Helvetica', '', 10)
    for row in [('Crop Farmers', '1,500', '207'), ('Mixed Farmers', '700', '97'), ('Livestock Farmers', '300', '42')]:
        for col in row:
            pdf.cell(60, 8, col, 1, 0, 'C')
        pdf.ln()
    pdf.ln(5)

    pdf.section_title('3.3 Data Collection Methods')
    pdf.body('This study will use the following primary methods of data collection:')

    pdf.sub_section_title('3.3.1 Questionnaires')
    pdf.body(
        'Structured questionnaires will be administered to the sampled farmers to gather data on their '
        'current crop selection practices, disease management experiences, and technology adoption '
        'capacity. Likert-scale questions will be used to assess user satisfaction after system testing. A '
        'sample questionnaire is attached as an appendix.'
    )

    pdf.sub_section_title('3.3.2 Interviews')
    pdf.body(
        'Semi-structured interviews will be conducted with five agricultural extension officers at the Meru '
        'County Agriculture Department to capture expert knowledge on common crop diseases and '
        'recommended treatments in the region. The interview guide is attached as an appendix.'
    )

    pdf.section_title('3.4 Development Tools and Materials')
    pdf.body('The system will be implemented using the following software tools and hardware specifications:')
    tools = [
        ('Programming Language:', 'Python 3.10'),
        ('Web Framework:', 'Flask 2.3'),
        ('ML Model - Crop Recommendation:', 'Scikit-learn (Random Forest Classifier)'),
        ('ML Model - Disease Detection:', 'TensorFlow / Keras (MobileNetV2 CNN)'),
        ('Database:', 'SQLite (development), PostgreSQL (production)'),
        ('Frontend:', 'HTML5, CSS3, JavaScript, Bootstrap 5'),
        ('Report Generation:', 'FPDF2 Python library'),
        ('Version Control:', 'Git / GitHub'),
        ('Hardware Requirements:', 'Minimum 8GB RAM, 2GHz CPU, GPU recommended for training'),
    ]
    for label, val in tools:
        pdf.bold_label(label, val)

    pdf.section_title('3.5 System Development Methodology')
    pdf.body(
        'The system will be developed using the Agile System Development Methodology. Agile is an '
        'iterative approach to software development that delivers working software in short cycles called '
        'sprints (Beck et al., 2001). Agile is appropriate for this project because requirements are expected '
        'to evolve based on user feedback during testing; it allows rapid iterations so that each module '
        '(authentication, crop recommendation, disease detection, report generation) can be developed and '
        'validated independently; and it supports collaborative development suitable for a student group project.'
    )

    pdf.section_title('3.6 System Design')
    pdf.body(
        'System design is the actual development of the system processes. The researcher provides an '
        'architectural design of the entire process. This study uses Use Case Diagrams and Data Flow '
        'Diagrams (DFDs) as the primary design tools.'
    )

    pdf.sub_section_title('3.6.1 Use Case Diagram')
    pdf.body(
        'The use case diagram illustrates the interactions between system actors (Farmer, Administrator) '
        'and the system. The primary use cases include: Register/Login, Input Soil Parameters for Crop '
        'Recommendation, Upload Leaf Image for Disease Detection, View Analysis History, and Download '
        'PDF Report. The use case diagram is presented in Figure 1 (see appendix).'
    )

    pdf.sub_section_title('3.6.2 Data Flow Diagram (DFD)')
    pdf.body(
        'The Level 0 DFD depicts the system as a single process receiving farmer inputs (soil data, leaf '
        'images) and producing outputs (crop recommendations, disease diagnoses, PDF reports). The '
        'Level 1 DFD decomposes this into sub-processes: User Authentication, Crop Recommendation '
        'Engine, Disease Detection Engine, Advisory Generator, and Report Generator. DFDs are presented '
        'in Figure 2 and Figure 3 (see appendix).'
    )

    pdf.section_title('3.7 Data Processing and Analysis')
    pdf.body(
        'Data processing involves editing, coding, classification, and tabulation of collected data. Editing '
        'ensures completeness of questionnaire responses; coding assigns numeric values to categorical '
        'answers; classification groups responses by farmer stratum; and tabulation summarizes data into '
        'frequency tables for analysis. This study will analyze data using descriptive and inferential statistics.'
    )

    pdf.sub_section_title('3.7.1 Descriptive Statistics')
    pdf.body(
        'Descriptive statistics including frequency distribution, percentages, and measures of central '
        'tendency (mean, median) will be used to describe farmers\' current practices and technology '
        'adoption levels. These will summarize Likert-scale responses on system usability and satisfaction. '
        'Graphical representations such as bar graphs and pie charts will be used to visualize results.'
    )

    pdf.sub_section_title('3.7.2 Inferential Statistics')
    pdf.body(
        'Correlation analysis will be used to determine the relationship between system usage frequency '
        'and crop yield improvement. A T-test will compare crop selection accuracy before and after '
        'system adoption to validate the system\'s effectiveness. ANOVA will be used to compare '
        'satisfaction levels across farmer strata (crop farmers, mixed farmers, and livestock farmers).'
    )

    pdf.section_title('3.8 Ethical Consideration')
    pdf.body(
        'Ethics are the norms or standards for conduct that distinguish between right and wrong. This '
        'study will uphold the following ethical principles throughout the research process:'
    )
    pdf.body(
        'Informed Consent: All participants will be briefed on the study purpose, their rights to withdraw, '
        'and how their data will be used before data collection begins. Confidentiality: No personally '
        'identifiable information will be published in the research findings. Data Integrity: All collected data '
        'will be accurately recorded without fabrication or falsification. Privacy: User data stored in the '
        'system will be protected with secure password hashing (bcrypt), encrypted sessions, and HTTPS '
        'enforcement to prevent unauthorized access.'
    )

    # ============================================================
    # CHAPTER 4: SYSTEM ANALYSIS
    # ============================================================
    pdf.add_page()
    pdf.chapter_heading('CHAPTER FOUR: SYSTEM ANALYSIS')

    pdf.section_title('4.0 Overview')
    pdf.body(
        'This chapter presents the system analysis for the Intelligent Crop Recommendation and Plant '
        'Disease Detection System. It covers the feasibility study conducted to establish the viability of the '
        'proposed system, a description of the current system and its limitations, a description of the '
        'proposed system, and detailed functional and non-functional system requirements.'
    )

    pdf.section_title('4.1 Feasibility Study')
    pdf.body(
        'A feasibility study is a preliminary analysis that determines the viability of developing a proposed '
        'system (Dennis et al., 2018). After carrying out a feasibility study on the existing agricultural '
        'advisory system, the following conclusions were drawn:'
    )

    pdf.sub_section_title('4.1.1 Technical Feasibility')
    pdf.body(
        'The proposed system relies on Python 3.10, Flask, Scikit-learn, and TensorFlow -- all of which are '
        'open-source and freely available. The pre-trained MobileNetV2 CNN model for disease detection '
        'can run on standard laptops with at least 4GB RAM. Smartphones with Android 8.0 and above can '
        'access the web application through any modern browser. Technical feasibility is therefore confirmed; '
        'the institution and the development team possess sufficient technical capacity to develop and '
        'deploy this system within the project timeline.'
    )

    pdf.sub_section_title('4.1.2 Economic Feasibility')
    pdf.body(
        'The development cost is minimal since all tools are open-source and the development team is '
        'composed of university students. Hosting costs are estimated at KES 3,000 per month on shared '
        'Linux hosting. The economic benefits, including reduced crop losses through timely disease '
        'intervention and improved yield through evidence-based crop selection, far outweigh the '
        'development and operational costs, confirming economic feasibility.'
    )

    pdf.sub_section_title('4.1.3 Legal Feasibility')
    pdf.body(
        "The system complies with Kenya's Data Protection Act (2019), which governs the collection, "
        'storage, and use of personal data. User data such as registration details and analysis history will '
        'be stored securely and not shared with third parties without explicit user consent. The system '
        'meets all legal and contractual requirements applicable in Kenya.'
    )

    pdf.sub_section_title('4.1.4 Operational Feasibility')
    pdf.body(
        'The system is designed with a simple, intuitive interface requiring no specialized technical training. '
        'Farmers familiar with basic smartphone usage will be able to operate the system within minutes of '
        'first use. The Flask web application is accessible via any browser, eliminating the need for '
        'device-specific installations. Operational feasibility is confirmed.'
    )

    pdf.section_title('4.2 Description of Current System')
    pdf.body(
        'Currently, smallholder farmers in Kenya rely on manual advisory services for crop selection and '
        'disease management. A farmer seeking crop advice must physically visit an agricultural extension '
        'office or wait for periodic field visits from extension officers -- a process that can take days or '
        'weeks, during which crop conditions may deteriorate. Disease identification is done through visual '
        'inspection by the farmer or an agronomist, which is subjective, time-consuming, and often '
        'inaccessible to remote rural communities. There is no digital record-keeping of analyses; each '
        'consultation starts from scratch. Fertilizer and treatment recommendations are communicated '
        'verbally, with no formal take-away report or documentation.'
    )

    pdf.sub_section_title('4.2.1 Limitations of the Current System')
    for label, val in [
        ('Geographic Inaccessibility:', 'Extension officers cannot reach all rural farmers regularly, creating advisory gaps in remote areas.'),
        ('Subjectivity:', 'Disease diagnosis depends entirely on the personal experience of the agronomist, leading to inconsistent advice.'),
        ('Lack of Integration:', 'Crop recommendation and disease detection are handled by different institutions with no shared platform.'),
        ('No Digital Records:', 'Farmers cannot track the history of their agricultural decisions or analyses over time.'),
        ('No Automated Reports:', 'Recommendations are verbal and not formally documented, making compliance tracking impossible.'),
        ('Time Delays:', 'The manual consultation process introduces delays that can result in uncontrollable disease outbreaks.'),
    ]:
        pdf.bold_label(label, val)

    pdf.section_title('4.3 Proposed System')
    pdf.body(
        'The proposed Intelligent Crop Recommendation and Plant Disease Detection System is a web-based '
        'platform that integrates: a Random Forest crop recommendation engine; a CNN plant disease '
        'detection module; a secure user authentication and registration system; analysis history tracking '
        'per user account; and an automated PDF report generation feature. The system is accessible '
        '24 hours a day, 7 days a week via any internet-enabled device, addressing all limitations of the '
        'current system. It provides objective, ML-powered advice, integrates multiple advisory functions '
        'within one platform, and maintains a digital record of all sessions for each registered user.'
    )

    pdf.section_title('4.4 Functional Requirements')
    pdf.body('The system shall support the following functional requirements:')
    for req_id, desc in [
        ('FR1:', 'Allow users to register and create secure personal accounts with unique credentials.'),
        ('FR2:', 'Authenticate registered users via email and password with secure session management.'),
        ('FR3:', 'Accept soil fertility parameters (N, P, K, pH, temperature, humidity, rainfall) and return the recommended crop with supporting advice.'),
        ('FR4:', 'Accept uploaded plant leaf images and return a disease diagnosis with a confidence score.'),
        ('FR5:', 'Display actionable disease management and fertilizer recommendations based on the diagnosis.'),
        ('FR6:', 'Allow users to view their historical crop recommendation and disease analysis records through a personal dashboard.'),
        ('FR7:', 'Generate and allow download of comprehensive PDF reports summarizing each analysis session.'),
    ]:
        pdf.bold_label(req_id, desc)

    pdf.section_title('4.5 Non-Functional Requirements')
    for label, desc in [
        ('Performance:', 'Crop recommendation results shall be returned within 2 seconds. Disease diagnosis shall complete within 5 seconds of image upload.'),
        ('Security:', 'User passwords shall be hashed using bcrypt. Sessions shall expire after 30 minutes of inactivity. All data transmission shall use HTTPS.'),
        ('Usability:', 'The interface shall be navigable by a user with basic smartphone literacy within 5 minutes of first use without additional training.'),
        ('Reliability:', 'The system shall maintain 99% uptime. A fallback color-pattern-based classifier shall be activated automatically if the CNN model is unavailable.'),
        ('Scalability:', 'The system shall support a minimum of 500 concurrent users without performance degradation.'),
        ('Maintainability:', 'The codebase shall be structured using modular Flask Blueprints to allow independent updating of each functional module.'),
    ]:
        pdf.bold_label(label, desc)

    # ============================================================
    # REFERENCES
    # ============================================================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 10, 'REFERENCES', 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 11)
    refs = [
        'Beck, K., et al. (2001). Manifesto for Agile Software Development. Agilemanifesto.org.',
        'Dennis, A., Wixom, B. H., & Tegarden, D. (2018). Systems Analysis and Design: An Object-Oriented Approach with UML. Wiley.',
        'Ferentinos, K. P. (2018). Deep learning models for plant disease detection and diagnosis. Computers and Electronics in Agriculture, 145, 311-318.',
        'Hughes, D. P., & Salathe, M. (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. arXiv:1511.08060.',
        'Kamilaris, A., & Prenafeta-Boldu, F. X. (2018). Deep learning in agriculture: A survey. Computers and Electronics in Agriculture, 147, 70-90.',
        'Kumar, R., et al. (2020). Crop recommendation system using machine learning. International Journal of Engineering Research & Technology.',
        'Liakos, K. G., Busato, P., Moshou, D., Pearson, S., & Bochtis, D. (2018). Machine learning in agriculture: A review. Sensors, 18(8), 2674.',
        'Mohanty, S. P., Hughes, D. P., & Salathe, M. (2016). Using deep learning for image-based plant disease detection. Frontiers in Plant Science, 7, 1419.',
        'Mucherino, A., et al. (2009). Data Mining in Agriculture. Springer US.',
        'Ramcharan, A., et al. (2017). Deep learning for image-based cassava disease detection. Frontiers in Plant Science, 8, 1852.',
        'Sharma, A., et al. (2021). Machine learning applications for precision agriculture. IEEE Access.',
        'Strange, R. N., & Scott, P. R. (2005). Plant disease: A threat to global food security. Annual Review of Phytopathology, 43, 83-116.',
    ]
    for i, ref in enumerate(refs, 1):
        pdf.cell(10, 7, f'{i}.', 0, 0)
        pdf.multi_cell(0, 7, ref)
        pdf.ln(2)


def generate_research_proposal():
    output_filename = 'Research_Proposal_Group3_Updated.pdf'
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)

    print("[1/2] Pass 1: Collecting page numbers...")
    pdf1 = ResearchProposal()
    build_document(pdf1, show_toc=False)

    print("[2/2] Pass 2: Generating final document...")
    pdf2 = ResearchProposal()
    build_document(pdf2, show_toc=True, toc_entries=pdf1.toc_data)
    pdf2.output(out_path)

    print(f"\n[OK] Success! PDF generated: {out_path}")
    return out_path


if __name__ == '__main__':
    generate_research_proposal()

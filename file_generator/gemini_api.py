import google.generativeai as genai
from .generateDoc import create_doc
from .generatePresentation import create_presentation
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="AIzaSyDOKweXGB9d3Ey9fcCRJkFjAxaCRju1NiQ")

model = genai.GenerativeModel('gemini-2.5-flash')
def ai_request(data):
    full_name = data['full_name']
    doc_type = data['doc_type']
    username = data['username']
    theme = data['theme']
    subject = data['subject']
    if doc_type == "word":
        request = 'Menga quyidagi mavzuda universitetdagi mustaqil ish uchun 20000 belgidan iborat matn qaytar. '
        request += "Matnda hech qanday yulduzcha, stikerlar bo'lmasin. Xatto ajratib ko'rsatish uchun ham yulduzchalardan foydalanma. "
        request += "Matnda faqat so'ralgan ma'lumotdan boshqa hatto sharh ham keltirilmasin. "
        request += f"Matnga mos reja tuz. Rejalar soni 4ta bo'lsin. Fan: {subject}, mavzu: {theme}"

        response = model.generate_content(request)
        response_text = response._result.candidates[0].content.parts[0].text
        result = create_doc(response_text, full_name, username, subject, theme)
        if result == 'ok':
            return 'ok'
        return 
    elif doc_type == 'powerpoint':
        request = f"Men taqdimot qilmoqchiman. Mavzu: {theme}. Menga presentatsiya uchun ma'lumotlar ber. "
        request += "Uni json formatda ber. masalan: {1:{'title': 'blabla', 'content':{''pointer1': 'anything', 'pointer2': '...', 'pointer3': '..'}}, 2:{...}} "
        request += "contentdagi pointerlar mavzu haqidagi ma'lumot bo'laklari. pointer1 da asosan keng tushunchalar 3 gap.  "
        request += "pointer2 va pointer3 qisqa tushuncha, eslatma, qismlar 1-2 gap.(70ta belgidan oshmasin.)  " 
        request += "Slide sahifalari soni 14ta. jsondan boshqa hech nima bo'lmasin "
        response = model.generate_content(request)
        response_text = response._result.candidates[0].content.parts[0].text
        f = open(f"{username}.txt", 'w')
        f.write(response_text)
        f.close()

        create_presentation(theme=theme, full_name=full_name, username=username)

        return 'ok'


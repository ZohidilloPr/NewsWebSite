from django.conf import settings
from rest_framework import status
from django.core.mail import send_mail
from django.utils.html import format_html

{
    "f_name": "Zohidillo Turg'unov",
    "email": "turgunovzohidillo77@gmail.com",
    "number": "+998332300701",
    "birth_day": "1994-10-01",
    "capital": "Andijon vil Baliqchi tum Chinobod shaxri",
    "appeal":"xazilashdimda endi mazgi",
    "to_email": "kurbanovotabek2001@gmail.com",
    "checkbox": "True" 
}


# class SendMessageToEmail():
#     """ MUROJATLAR JONATISH UCHUN """
#     def post(self, request, *args, **kwargs):
#         subject = "Onlayn murojat"
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = []
#         serializer = AppealSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             f_name = data.get("f_name")
#             email = data.get("email")
#             number = data.get("number")
#             capital = data.get("capital")
#             birth_day = data.get("birth_day")
#             appeal = data.get("appeal")
#             to_email = data.get("to_email")
#             checkbox = data.get("checkbox")
#             time = data.get("time")
#             recipient_list.append(to_email)
#             message = format_html(
#                 f"Murojat yuborgan shaxs: \n\tIsm: {f_name}\nBog'lanish uchun: \n\tE-pochta: {email} \n\tTelefon raqam: {number} \
#                 \nYashash manzili: \n\tHudud: {capital}\nTug'ulgan sanasi: {birth_day} \
#                 \n\n\n Murojat mazmuni: \n{appeal} \n\nShartlarga ro'ziligi: {checkbox} \n\nShartlarga ro'ziligi: {time}", )
#             send_mail(
#                 subject,
#                 message,
#                 from_email,
#                 recipient_list,
#                 fail_silently=False,
#             )
#             appeal_m = Appeal.objects.create(
#                 email=email,
#                 number=number,
#                 f_name=f_name,
#                 appeal=appeal,
#                 capital=capital,
#                 to_email=to_email,
#                 checkbox=checkbox,
#                 birth_day=birth_day,
#             )
#             appeal_m.save()
#             return Response({"success": "True"}, status=status.HTTP_200_OK)
#         return Response({"success": "False"}, status=status.HTTP_400_BAD_REQUEST)
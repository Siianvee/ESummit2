from django.shortcuts import render, redirect
from .models import Registration
import uuid
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import qrcode
from io import BytesIO
import json


def home(request):
    sponsors = [
        {'name': 'Tata Advanced Systems',
         'logo_url': 'https://pbs.twimg.com/profile_images/1200315900605300736/eUSE4wB2_400x400.jpg'},
        {'name': 'NASSCOM',
         'logo_url': 'https://nasscom.in/sites/default/files/styles/webp/public/media/media_kit/media_kit_2_7.jpg.webp?itok=9XtNFpgJ'},
        {'name': 'Google X',
         'logo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxwtgnrqu-dttASyAeEQLGBmwfb8K8H_QziQ&s'},
        {'name': 'SoftBank Vision Fund',
         'logo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqXMUcL9Nmi9G1HbyMI1DvWdl47AJaRC6_1w&s'},
        {'name': 'SpaceX', 'logo_url': 'https://www.spacex.com/static/images/share.jpg'},
    ]

    partners = [
        {'name': 'Gravity Industries',
         'logo_url': 'https://yt3.googleusercontent.com/ytc/AIdro_lf9L-vyM-NbF-PZ57nZO-G-mmQvWpTucutE3dZr2ZCKQ=s900-c-k-c0x00ffffff-no-rj'},
        {'name': 'Hacksmith Industries',
         'logo_url': 'https://yt3.googleusercontent.com/KFB53wRenII7VQEYIER3-sRL0J9jttv8dRwPk8Rie9mpCmQZqBt1fDhSQBk7SVNdLlaZW0_aJQ=s160-c-k-c0x00ffffff-no-rj'},
        {'name': 'Drone Federation of India',
         'logo_url': 'https://s3-us-west-2.amazonaws.com/cbi-image-service-prd/modified/92588bf2-b3a2-4354-a283-d8d6b5b5968b.png'},
        {'name': 'YourStory',
         'logo_url': 'https://images.seeklogo.com/logo-png/52/1/yourstory-logo-png_seeklogo-524486.png'},
        {'name': 'TechCrunch India',
         'logo_url': 'https://seeklogo.com/images/T/techcrunch-logo-B444826970-seeklogo.com.png'},
        {'name': 'Inc42',
         'logo_url': 'https://cdn.dribbble.com/users/873027/screenshots/3996894/attachments/914616/dribbble_001_02.png'},
        {'name': 'WeWork India',
         'logo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSU3jicICb3JF3Y1_2fFDs2odj24nrRsClC-w&s'},
        {'name': 'NASSCOM',
         'logo_url': 'https://nasscom.in/sites/default/files/styles/webp/public/media/media_kit/media_kit_2_7.jpg.webp?itok=9XtNFpgJ'},
        {'name': 'Invest India',
         'logo_url': 'https://static.investindia.gov.in/s3fs-public/2019-10/logo-investindia.png'},
        {'name': 'Indian Angel Network',
         'logo_url': 'https://pbs.twimg.com/profile_images/475468285912154113/q74dzrAx_400x400.jpeg'},
    ]

    panels = [
        {
            'topic': 'Sky High: Redefining Urban Mobility with Air Taxis and Drones',
            'description': 'Advancements in urban air mobility.',
            'panelists': [
                {'name': 'Somnath S', 'position': 'Chairman, ISRO',
                 'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/0/06/S._Somanath%2C_Director_of_VSSC%2C_ISRO%2C_speaks_during_the_Heads_of_Agency_Plenary_of_the_70th_International_Astronautical_Congress_%28cropped%29.jpg'},
                {'name': 'Gopal Vittal', 'position': 'CEO, Airtel',
                 'photo_url': 'https://www.iimcal.ac.in/sites/default/files/styles/medium/public/images/gopal_vittal_0.jpg?itok=GuN4RHJn'},
                {'name': 'Tanay Manjrekar', 'position': 'Head of Propulsion, Odys Aviation',
                 'photo_url': 'https://mumbaimirror.indiatimes.com/photo/79162006.cms'},
                {'name': 'Kanika Tekriwal', 'position': 'CEO, JetSetGo',
                 'photo_url': 'https://im.rediff.com/getahead/2022/dec/02kanika-tekriwal3.jpg'},
                {'name': 'Kashyap Deorah', 'position': 'CEO, HyperTrack',
                 'photo_url': 'https://acr.iitbombay.org/wp-content/uploads/2024/03/DAA300x300_0011_KashyapDeorah.jpg'},
            ]
        },
        {
            'topic': 'Taking Flight: The Next Generation of Wearable Tech for Personal Mobility',
            'description': 'Personal mobility and next-gen tech.',
            'panelists': [
                {'name': 'Richard Browning', 'position': 'Founder, Gravity Industries',
                 'photo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTinH4PGZU7HIvyZ-YVNPtQaekSkPmg22cxEQ&s'},
                {'name': 'James Hobson', 'position': 'Founder, HackSmith Industries',
                 'photo_url': 'https://media.licdn.com/dms/image/C5603AQGQMpDgP5vjwA/profile-displayphoto-shrink_200_200/0/1517621048797?e=2147483647&v=beta&t=9tXqMIGqMTXO7iaPl_Py1epx1e5mVxCmFzBZq1xvdXo'},
                {'name': 'A. S. Kiran Kumar', 'position': 'Former ISRO Chairman',
                 'photo_url': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTEyA7TKKvTYb16i4yHGoMeI3qsz2om0gnCK2v67DDw1KpAww_J'},
                {'name': 'B. N. Suresh', 'position': 'Chairman, IIST',
                 'photo_url': 'https://www.iist.ac.in/sites/default/files/chancellorphoto/sureshsir.jpg'},
                {'name': 'Pavan Kumar', 'position': 'Researcher, National Aerospace Laboratory',
                 'photo_url': 'https://www.nal.res.in/sites/default/files/2022-01/pavan%20kumar.jpg'},
            ]
        },
        {
            'topic': 'Investing in Tomorrow: Navigating the Future of Mobility Startups',
            'description': 'A future for mobility startups.',
            'panelists': [
                {'name': 'Sanjay Mehta', 'position': 'Investor, Indian Angel Network',
                 'photo_url': 'https://media.licdn.com/dms/image/v2/C5103AQFKnhfipB_99A/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1563262664331?e=1736380800&v=beta&t=tPCGFgBoSp8CqFep8SkF2t2WhcAkcmNVNUS7AaKT87E'},
                {'name': 'Deep Nishar', 'position': 'Investor, SoftBank',
                 'photo_url': 'https://media.licdn.com/dms/image/v2/C4E03AQF5HQGb36-lEA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1516227300189?e=1736380800&v=beta&t=k2qyQvM1FEuFUvkIxm92HWy7mNNniZpd6_aGJ6wy1AY'},
                {'name': 'Ritesh Agarwal', 'position': 'Founder, OYO',
                 'photo_url': 'https://media.licdn.com/dms/image/v2/C4D03AQEijuEmdjNrqw/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1609836256686?e=1736380800&v=beta&t=v2hMqjTT4kTjOxch7RzzjkCQ-FdR3k91Ubk56F8Q_Kc'},
                {'name': 'Kiran Mazumdar Shaw', 'position': 'Exec Chairperson, Biocon',
                 'photo_url': 'https://media.licdn.com/dms/image/v2/C4D03AQEJ7awsy78NEA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1663845727341?e=1736380800&v=beta&t=ooC5Esf5iaUedQPTWO_moS9T3BTQuorEzynBgxgtY3s'},
                {'name': 'Ashish Gupta', 'position': 'Partner, Helion',
                 'photo_url': 'https://d18oqps9jq649a.cloudfront.net/public/assets/16359257681635925768Dr%20Ashish%20Gupta.png'},
            ]
        },
    ]

    return render(request, 'home.html', {
        'sponsors': sponsors,
        'partners': partners,
        'panels': panels,
    })


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        # Check if email is already registered
        if Registration.objects.filter(email=email).exists():
            return redirect('already_registered')  # Redirect if email is registered

        # Generate a unique ticket code
        ticket_code = str(uuid.uuid4())[:8]

        user = Registration.objects.create(name=name, email=email, phone=phone, ticket_code=ticket_code)

        user_data = {
            "name": user.name,
            "ticket_id": user.ticket_code,
            "email": user.email,
            "phone": user.phone,
        }

        # Generate QR code for the ticket code
        qr_data = json.dumps(user_data)
        qr = qrcode.make(qr_data)
        qr_io = BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)

        # Prepare email
        subject = 'Your E-Summit Ticket Confirmation'
        from_email = settings.EMAIL_HOST_USER
        to_email = email

        # Render HTML content for email
        html_content = render_to_string('email_templates/ticket_email.html', {
            'user': user,
            'ticket_code': ticket_code
        })

        # creating email object with HTML content
        email = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.attach(f"{name}_QR_Ticket.png", qr_io.getvalue(), "image/png")
        email.send()

        return redirect('confirmation')

    return render(request, 'register.html')


def confirmation(request):
    return render(request, 'confirmation.html')


def already_registered(request):
    return render(request, 'already_registered.html')


def fetch_ticket(request):
    if request.method == 'POST':
        email = request.POST['email']

        # Check if the email is registered
        try:
            user = Registration.objects.get(email=email)
        except Registration.DoesNotExist:
            # Redirect to an error page or show a notification if email is not registered
            return redirect('email_not_found')  # Create an 'email_not_found' page or use a notification

        # Generated user data
        user_data = {
            "name": user.name,
            "ticket_id": user.ticket_code,
            "email": user.email,
            "phone": user.phone,
        }

        # Generate QR code for the ticket code
        qr_data = json.dumps(user_data)
        qr = qrcode.make(qr_data)
        qr_io = BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)

        # Prepare email
        subject = 'Your E-Summit Ticket'
        from_email = settings.EMAIL_HOST_USER
        to_email = email

        # Render HTML content for email
        html_content = render_to_string('email_templates/ticket_email.html', {
            'user': user,
            'ticket_code': user.ticket_code
        })

        # Create email object with HTML content
        email = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")

        email.attach(f"{user.name}_QR_Ticket.png", qr_io.getvalue(), "image/png")
        email.send()

        return redirect('confirmation')

    return render(request, 'fetch_ticket.html')

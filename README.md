## VolunteerHub

VolunteerHub is a Django web application that brings different volunteering opportunities together in one place.

Users can create an account, browse active opportunities, filter them by category, apply for roles, view their applications, update their profile, send messages to other users, and reset a forgotten password by email.

The project was created for my Frameworks module and uses Django, PostgreSQL, Bootstrap, JavaScript, Render, and Brevo.

---

## Why I Chose This Project

I chose to create VolunteerHub because I had not really come across a simple website where different types of volunteering opportunities were available together in one place.

Usually, someone looking to volunteer may have to visit several different charity or organisation websites to find suitable opportunities. I thought it would be useful to create one central platform where users could browse different types of volunteer work, view details, apply, and keep track of their applications.

I also felt the idea suited the module well because it allowed me to work with authentication, database relationships, forms, JavaScript, messaging, email recovery, testing, security, and deployment as part of one complete project.

---

## Main Features

VolunteerHub includes:

- User registration, login and logout.
- Profile editing.
- Active volunteering opportunities.
- Opportunity detail pages.
- Opportunity categories.
- JavaScript category filtering.
- Volunteer applications.
- Duplicate application prevention.
- Application statuses: Pending, Approved and Rejected.
- A My Applications page.
- Internal user messaging.
- Inbox and message archiving.
- Password reset by email.
- Django Admin for managing opportunities and applications.
- Responsive Bootstrap styling.

---

## Volunteering Opportunities

Each opportunity stores information such as:

- Title.
- Organisation.
- Location.
- Date.
- Spaces available.
- Description.
- Category.
- Active status.

Only active opportunities are displayed to users.

The deployed version contains sample volunteering opportunities around Dublin for demonstration purposes.

---

## Opportunity Categories

Opportunities can be assigned to categories including:

- Community.
- Charity.
- Food Support.
- Environment.
- Education.
- Other.

A JavaScript filter allows users to select a category and immediately update the displayed opportunities without reloading the page.

---

## Applications

Logged-in users can apply for opportunities.

Each application stores:

- The user.
- The selected opportunity.
- An optional message.
- Application status.
- Date applied.

Users can view their applications on the **My Applications** page.

Administrators can change application statuses to:

- Pending.
- Approved.
- Rejected.

A database constraint prevents the same user from applying for the same opportunity more than once.

---

## Messaging

VolunteerHub includes an internal messaging system.

Registered users can:

- Send messages to other users.
- Receive messages.
- View messages in their inbox.
- Archive messages.

The archive view checks that the logged-in user is actually the recipient of the message before allowing it to be archived.

---

## Password Reset

VolunteerHub includes Django's forgotten-password functionality.

Users with an email address connected to their account can request a password reset email and follow the secure link to choose a new password.

During development, reset emails were initially displayed in the terminal using Django's console email backend.

For the deployed project, real email delivery was configured using Brevo and django-anymail.

---

## Technologies Used

### Backend

- Python
- Django
- PostgreSQL
- dj-database-url
- Gunicorn

### Frontend

- HTML
- CSS
- Bootstrap 5
- JavaScript

### Deployment and Email

- Render
- Render PostgreSQL
- WhiteNoise
- Brevo
- django-anymail

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Git Bash
- Django Admin

---

## Database Structure

The main models used in the project are:

### Opportunity

Stores the volunteering opportunities shown on the website.

Important fields include:

- `title`
- `organization`
- `location`
- `date`
- `spaces_available`
- `description`
- `category`
- `is_active`

### Application

Connects a registered user to an opportunity.

Important fields include:

- `user`
- `opportunity`
- `message`
- `status`
- `applied_on`

A uniqueness constraint prevents duplicate applications.

### Message

Stores messages sent between registered users.

Important fields include:

- `sender`
- `recipient`
- `subject`
- `body`
- `sent_at`
- `archived`

---

## Security

Sensitive settings are stored using environment variables rather than directly in the source code.

The project uses environment variables for:


SECRET_KEY
DEBUG
DATABASE_URL
BREVO_API_KEY
DEFAULT_FROM_EMAIL


## Manual Testing

The deployed application was manually tested to confirm that the main features worked correctly.

- Registration - Passed
- Login and logout - Passed
- Profile editing - Passed
- Opportunity listing - Passed
- Opportunity details - Passed
- Category filtering - Passed
- Application submission - Passed
- Duplicate application prevention - Passed
- My Applications - Passed
- Admin application status updates - Passed
- Sending messages - Passed
- Inbox - Passed
- Message archiving - Passed
- Password reset email - Passed
- Responsive navigation - Passed

---

## Troubleshooting and Challenges

Several issues appeared during development and deployment. Solving these problems was an important part of completing the project.

### Moving From SQLite to PostgreSQL

When the application was first deployed, the website loaded correctly but displayed no active opportunities.

The reason was that the Render PostgreSQL database was separate from my local SQLite database. Running migrations created the database structure but did not copy my local records.

I solved this by creating a production superuser and adding sample volunteering opportunities through Django Admin.

### Creating a Production Superuser

My local administrator account did not exist in the live PostgreSQL database.

I temporarily connected my local Django project to the Render PostgreSQL database and ran:


python manage.py createsuperuser


After creating the live administrator, I removed the production database connection from my local environment.

### Password Reset URL

The accounts application uses a URL namespace, which caused an issue with the password reset confirmation link.

I created a custom password reset email template using:

accounts:password_reset_confirm


This corrected the reset link.

### Brevo Email Configuration

The password reset feature originally used Django's console email backend during development.

For the deployed version I changed this to Brevo using `django-anymail`.

This involved:

- Creating and verifying a Brevo sender.
- Creating an API key.
- Configuring Anymail in Django.
- Storing the API key using environment variables.
- Adding the required environment variables to Render.

### Email Worked Locally but Not on Render

A direct email test from my local Django terminal worked, but password reset emails initially did not arrive from the deployed application.

Brevo's logs showed the local test email but no password reset email from Render.

I discovered that Render had not yet deployed the latest GitHub commit containing the Brevo configuration.

Once the latest commit was deployed, password reset emails worked correctly.

This was useful because it showed me the importance of checking which version of the code is actually running in production.

### Render Domain Verification

While setting up Brevo, I initially tried to verify the `onrender.com` domain.

I realised that the Render domain belongs to Render and I do not control its DNS records.

Instead, I used a verified sender email address through Brevo.

### Secret Key Security

During deployment preparation I noticed that the Django secret key had previously been stored directly in `settings.py`.

I changed the project to load it from an environment variable:


SECRET_KEY = os.environ["SECRET_KEY"]

I then generated a new secret key and updated both the local environment and Render environment variables.

The `.env` file is excluded from Git.

### Windows and Linux Line Endings

The project was developed on Windows but deployed through Render.

Git displayed a warning about the line endings in `build.sh`.

I added the following to `.gitattributes`:


*.sh text eol=lf


This keeps the deployment shell script compatible with Linux.

### Duplicate Applications

The project needed to prevent users from applying for the same opportunity more than once.

This was handled through application logic and a database uniqueness constraint.

An automated test confirms that duplicate applications are not created.

### Message Security

The archive feature needed to prevent users from archiving another person's messages.

The archive view checks both the message ID and the logged-in recipient.

An automated test confirms that another user cannot archive a message they do not own.

---

## Future Improvements

If I continued developing VolunteerHub, I would consider adding:

- Search by opportunity title or location.
- Organisation accounts.
- Allowing organisations to create their own opportunities.
- Email notifications when applications are approved or rejected.
- Favourite or saved opportunities.
- A dedicated archived messages page.
- Pagination.
- Better tracking of available spaces.
- User profile pictures.

For this version I focused on completing and testing the main project requirements rather than adding unnecessary features close to submission.

---

## Known Limitations

- The volunteering opportunities on the deployed site are sample portfolio data rather than live vacancies.
- The Render free service may take longer to load after a period of inactivity.
- The current version does not include separate organisation accounts.
- Messaging is internal to VolunteerHub rather than being sent by email.

---

## Credits

Technologies and services used include:

- Django
- Bootstrap
- PostgreSQL
- Render
- Brevo
- django-anymail
- WhiteNoise
- Gunicorn
- Git
- GitHub

Documentation used during development included Django, Bootstrap, Render, Brevo and django-anymail documentation.

---

## Project Links

LIVE APPLICATION

https://volunteerhub-mod5.onrender.com/

GITHUB REPOSITORY

https://github.com/mdpos95-tech/volunteerhub_MOD5

DJANGO ADMIN

https://volunteerhub-mod5.onrender.com/admin/

Admin login details are not included publicly in this README.

The administrator username and password required for assessment are supplied separately in the private LMS submission comments.

---

## Author

Mark O'Shea

Frameworks Portfolio Project

VolunteerHub
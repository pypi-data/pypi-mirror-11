# WebPortfolio

A batteries included Flask based framework to rapidly develop web applications 
or API endpoints. 

It comes with User Login section, Admin section to quickly get you going.

Also it includes a CMS admin, to quickly post blogs, create dynamic pages on the site.

Version: 0.0.*

## Install

    pip install webportfolio --process-dependency-links
    
## Create a project

    cd your_dir 
    
    webportfolio new -p wwww
    
## Setup Project
    
    cd your_dir 
    
    python manage.py setup
    
### Start your server

    webportfolio serve -p 

Go to http://your-domain/

---
    
## Why Flask?

Because Flask is fun, and you will still feel like you are writing. Explicity


## Why not Django? 

Because it's not Django. That's it! 


## Decision Made for You

- automatically generates routes based on the methods in your views

- Class name as the base url, ie: class UserAccount will be accessed at /user-account

- Auto route can be edited with @route()

- Restful: GET, POST, PUT, DELETE

- API Ready

- bcrypt is chosen as the password hasher

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- ORM: Active Alchemy (SQLALchemy wrapper)

- ReCaptcha

- csrf on all POST

- CloudStorage: Local, S3, Google Storage

- mailer (SES or SMTP)

- Caching

- Recaptcha

- Propel for deployment



# Built-in Modules 

- Basic Layout

- Index page

- Login, Signup, Lost Password, Account Settings page

- User Admin

- CMS Post Admin (To manage posts (article, blog, dynamic pages))

- Post Reader (To read post)

- Contact Page

- Error Page (Custom error page)

- Social Signin (in experiment)

- Social Share

- Bootswatch

- Font-Awesome

- Markdown


# Front End Components

- Lazy load images

- Social Share Buttons


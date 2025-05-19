# Bungalow Take Home Project for Backend Developer Role

## About This Project
This is a Django based assignment. We have created a base project for you to work from. 
You are free to vary from our original base if you would like to. We provide it with the intention of providing 
a common base for all candidates to work from and to hopefully save you a bit of time. 

If you need an introduction to Django, their docs are an excellent place to start: https://docs.djangoproject.com/en/3.2

We encourage you to use the Django Rest Framework for developing your API. This is a framework that we use extensively 
at Bungalow, and it provides some nice functionality out of the box. https://www.django-rest-framework.org/

## What to Build
We would like you to build an API that can be used to query some information about houses.
Sample data is provided in the `sample-data` folder.
We have provided the stub for a Django command to import the data. Finish writing this code.
You should use Django's ORM to model the data and store it in a local database.
Then, utilize the Django Rest Framework to provide an API to query the models.
A very basic API design here would simply return all of the data available.
You can choose to improve and refine this very basic API design, and we encourage you to do so.
This will give us an opportunity to see how you approach API design.
If you are running out of time, you can outline how you would have done things differently given more time.


## How Will This Be Evaluated
We will use this project as our basis for our evaluation of your coding skill level as it relates to our team.
To do this, we will review your code with an eye for the following:

- Design Choices - choice of functionality, readability, maintainability, extendability, appropriate use of language/framework features
- Does it work as outlined
- Testing - have you considered how you'd test your code?
- Documentation - have you provided context around decisions and assumptions that you have made?
- Polish - have you produced something that would be ready to go into a production system?
  if not, have you clearly stated what would be needed to get from where it is to that level of polish?

## Time Expectations
We know you are busy and likely have other commitments in your life, so we don't want to take too much of your time.
We don't expect you to spend more than 2 hours working on this project. That being said, if you choose to put more or
less time into it for whatever reason, that is your choice. Feel free to indicate in your notes below if you worked on
this for a different amount of time and we will keep that in mind while evaluating the project. You can also provide us
with additional context if you would like to. Additionally, we have left a spot below for you to note. If you have ideas 
for pieces that you would have done differently or additional things you would have implemented if you had more time, 
you can indicate those in your notes below as well, and we will use those as part of the evaluation. For example, if you 
would have tested more, you can describe the tests that you would have written, and just provide 1 or 2 actual implemented
tests.

## Public Forks
We encourage you to try this project without looking at the solutions others may have posted. This will give the most
honest representation of your abilities and skills. However, we also recognize that day-to-day programming often involves 
looking at solutions others have provided and iterating on them. Being able to pick out the best parts and truly 
understand them well enough to make good choices about what to copy and what to pass on by is a skill in and of itself. 
As such, if you do end up referencing someone else's work and building upon it, we ask that you note that as a comment. 
Provide a link to the source so we can see the original work and any modifications that you chose to make. 

## Setup Instructions
1. Fork this repository and clone to your local environment. If you make your fork private, please give access to the `bungalow-engineering` user. 
1. Install a version of Python 3 if you do not already have one. We recommend Python 3.8 or newer.
1. You can use the built-in virtual environment creation within Python to create a sandboxed set of package installs. 
   If you already have a preferred method of virtualenv creation, feel free to proceed with your own method. 
   `python -m venv env`    
1. You will need to activate your virtual environment each time you want to work on your project. 
   Run the `activate` script within the `env/bin` folder that was generated.
1. We have provided a `requirements.txt` file you can use to install the necessary packages.
   With your virtualenv activated run: `pip install -r requirements.txt`
1. To run the django server run `python manage.py runserver`
1. To run the data import command run `python manage.py import_house_data`
1. You are now setup and ready to start coding. 


# Your Notes
## Setup required:
1. Install python 3.12 (3.13 removes the entire cgi module, which causes problems), e.g.
```
pyenv install 3.12
pyenv local 3.12
```

Confirm the version is correct with `python --version`

2. Setup virtualenv and install dependencies
```
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Navigate to the listings folder (and for all future django commands)
`cd listings`

4. Apply migrations
`python manage.py migrate`

5. Load data
`python manage.py import_house_data ../sample-data/data.csv`

6. Add your OpenAI API key to the settings.py file

7. Run the server
`python manage.py runserver`

## Test Live
- This is currently deployed live, available for you to test, at https://bungalow.abdominusveritas.com. Three quick methods to try it out:
  - Open browser and go to: [https://bungalow.abdominusveritas.com/api/v1/properties/](https://bungalow.abdominusveritas.com/api/v1/properties/)
  - Via curl with `curl -X GET https://bungalow.abdominusveritas.com/api/v1/properties/`
  - Via the `api.http` file in your editor (e.g. VSCode) with the REST Client extension installed. 
    - Open the `api.http` file and click on the "Send Request" link to test the API.
- It will be deployed on my home server until the presentation
  - Deployed as a systemctl service, exposed to the internet over a cloudflare proxy

## How the API works
- All API endpoints are under a versioned path: `/api/<version>/...`
    - We default to `v1`

### Endpoints
- List properties: `GET /api/v1/properties/`
    - Returns a list of all properties
- Retrieve Property: `GET /api/v1/properties/{pk}/`
    - Fetch a single property by its primary key (id).
- Search Properties: `GET /api/v1/properties/?search=<term>`
    - You can perform simple full-text search on address, city, and home_type
- Filtering & Ordering:
  - You can filter on any of these fields:
  ```
  area_unit, bathrooms, bedrooms, home_size, home_type,
    last_sold_date, last_sold_price, link, price, property_size,
    rent_price, rentzestimate_amount, rentzestimate_last_updated,
    tax_value, tax_year, year_built, zestimate_amount, zestimate_last_updated,
    zillow_id, address, city, state, zipcode
  ```
  - Exact match: `GET /api/v1/properties/?city=West%20Hills&bedrooms=4`
  - Ordering on the same fields: GET `/api/v1/properties/?ordering=-last_sold_price`
- Pagination:
  - By default the list endpoint returns:
  ```
  {
  "count": <total>,
  "next": "<url or null>",
  "previous": "<url or null>",
  "results": [ ... ]
    }
  ```
  Page size is 20 by default. Use ?page=<page> to navigate.
- LLM-Powered Free-Text Query: 
    ```
    POST /api/v1/properties/ai-query/
    Content-Type: application/json
    
    {
      "query": "top 5 most expensive houses built after 1980 in West Hills"
    }
    ```
    - Input: arbitrary user text
    - Output: JSON array (or paginated results) of matching properties
    - How it works:
      - Sends your text to OpenAI's gpt-4.1-mini
      - Receives a Django-ORM filter dict (and optional _ordering, _limit)
      - Executes .filter(), .order_by(), and slicing in the viewset
- Examples exist for each API in the [api.http](api.http) file. 
  - You can use the REST Client extension in VSCode / PyCharm to run them directly from the editor.

## Testing
`python manage.py test api`

## Time Spent
*Give us a rough estimate of the time you spent working on this. If you spent time learning in order to do this project please feel free to let us know that too.*
*This makes sure that we are evaluating your work fairly and in context. It also gives us the opportunity to learn and adjust our process if needed.*

I probably spent between 2 and 3 hours doing this. I have never used Django before, so I did a bit of googling / chat gpt to get up to speed on the basics of how it works.

## Assumptions
*Did you find yourself needing to make assumptions to finish this?*
*If so, what were they and how did they impact your design/code?*

I needed to make a significant amount of product use-case and requirements in order to design this API. In the absence of a specific company's use case, I decided to optimize for:
- Simplicity to build. Less time spent writing the code, less code overall. Partially because this is a take-home interview, and partially because simpler and faster is better in the absence of specific requirements and the ability to clarify them.
- Simplicity to use. Follows standard REST patterns, and is easy to understand. I considered alternatives like GraphQL, gRPC / protocol buffers, or even a custom DSL, but they all add unnecessary complexity to the API and the client at this stage of development.
- In the interest of showing off a feature using an LLM to convert free-text queries into data retrieval code, I made the assumption that this would be a useful feature for the target market of this product. 

## Next Steps
*Provide us with some notes about what you would do next if you had more time.* 
*Are there additional features that you would want to add? Specific improvements to your code you would make?*
### Features
- I would want to speak more with the product leader to understand the use case and requirements for this API. It's unclear whether it's important to optimize for throughput, latency, flexibility, or developer productivity. It's also unclear how this software may need to evolve over time, which makes it more difficult to design the code in the optimal manner.

### Testing
- I did not write a comprehensive suite of tests for this project. Instead, I lightly cover the happy path in order to demonstrate working unit tests with simple examples that provide the most bang for the buck.
- With more time, I'd include the following:
  - Handle bad inputs
  - Handle all core APIs and pathways (via the query parameters)
  - Separate LLM testing on the prompt
  - Randomly generated data with property testing to cover edge cases more thoroughly
  - End-to-end tests (e.g. via HTTP in Docker) that spin up the full stack and hit the live API

### Anything else needed to make this production ready?
- Logging
- Linting
- Monitoring
- Error handling
- Authentication
- Rate limiting / throttling
- Admin portal frontend to manage the data
  - A process to keep the underlying data up to date
- More comprehensive testing
- Run on a production server, rather than a development one
- Autoscaling to handle spikes in traffic
- CI/CD (e.g. github actions)
  - Linting, tests, and security scans on every PR
  - Build and push docker images on merge
  - Automated deploys to staging / prod
- Secret management
- API documentation (beyond the default django one)

## How to Use
Included above in the notes section.

from linkedin_py.client import LinkedinClient
from linkedin_py.utils import prepare_url


profile_data_full_params = """
    :(id,first-name,last-name,headline,picture-url,industry,summary,specialties,
    positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),
    educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),
    associations,interests,num-recommenders,date-of-birth,
    publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),
    patents:(id,title,summary,number,status:(id,name),
    office:(name),inventors:(id,name),date,url),
    languages:(id,language:(name),proficiency:(level,name)),
    skills:(id,skill:(name)),certifications:(id,name,authority:(name),
    number,start-date,end-date),courses:(id,name,number),
    recommendations-received:(id,recommendation-type,recommendation-text,recommender),
    honors-awards,three-current-positions,three-past-positions,volunteer)
    """


def retrieve_profile_data(token, params=profile_data_full_params):
    """
    In default function returns all data what Linkedin returns for profile endpoint.
    To change this you need to modify `params` parameter.
    """
    url = prepare_url("https://api.linkedin.com/v1/people/~", params)
    request = LinkedinClient(token, url)

    return request.retrieve()


def retrieve_data(token, url, params=None):
    """
    Universal method to retrieve data from Linkedin API.
    """
    url = prepare_url(url, params)
    request = LinkedinClient(token, url)

    return request.retrieve()

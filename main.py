from datetime import datetime

from entities import Event, Company, CompanyCompetitor, CompanyForWebinar, CRAWLING_STATUSES
from notifier import Notifier

if __name__ == '__main__':

    # init objects
    # Company Competitor
    original_company_competitor_obj = None

    company_competitor_obj = CompanyCompetitor(
        company='brew',
        competitor='klue',
    )

    # Company
    original_company_obj = Company(
        employees_min=1,
        employees_max=3,
        link='www.google.com',
        name='event test',
    )

    company_obj = Company(
        employees_min=1,
        employees_max=3,
        link='www.google.com',
        name='event test',
        last_crawled=CRAWLING_STATUSES.TEXT_ANALYZED,
        is_deleted=True
    )

    # Event
    original_event_obj = Event(
        start_date=datetime.now(),
        link='www.google.com',
        name='event test',
    )

    event_obj = Event(
        start_date=datetime.now(),
        link='www.google.com',
        name='event test',
        is_blacklisted=True
    )

    # Company For Webinar
    original_company_for_webinar_obj = CompanyForWebinar(
        webinar='Python',
        company='Brew',
    )

    company_for_webinar_obj = None

    # init Notifiers

    event_notifier = Notifier(
        original_entity_obj=original_event_obj,
        entity_obj=event_obj
    )

    company_notifier = Notifier(
        original_entity_obj=original_company_obj,
        entity_obj=company_obj
    )

    company_competitor_notifier = Notifier(
        original_entity_obj=original_company_competitor_obj,
        entity_obj=company_competitor_obj
    )

    company_for_webinar_notifier = Notifier(
        original_entity_obj=original_company_for_webinar_obj,
        entity_obj=company_for_webinar_obj
    )

    event_notifier.notify()
    company_notifier.notify()
    company_competitor_notifier.notify()
    company_for_webinar_notifier.notify()

    # test for an entity_object with a list
    list_comp = ['Hello', 'Goodbye']
    different_objects_notifier = Notifier(
        original_entity_obj=list_comp,
        entity_obj=company_competitor_obj
    )

    different_objects_notifier.notify()

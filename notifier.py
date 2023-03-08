from typing import Any

from entities import *
from consts import *


class Notifier:
    """
    A class for comparing two objects from ENTITY_TYPES list
    Usage:
        1. Declaration of two objects for comparison
        2. Init a Notifier object with your declared objects | notifier = Notifier(original_event_obj, event_obj)
        3. Call notify() function and wait for results | notifier.notify()
    """
    _entity_obj: Any
    _original_entity_obj: Any

    _entity_obj_type: str = ''
    _original_entity_obj_type: str = ''

    _notify_string: str

    def __init__(self, entity_obj, original_entity_obj):
        self._entity_obj = entity_obj
        self._original_entity_obj = original_entity_obj
        self._notify_string = ''

    def notify(self) -> Optional[str]:
        """
        In case of a change on one from given objects this functions will notify to the user about the change
        :return: string represents the notification with all the relevant details
        """
        self._entity_obj_type = self._check_obj_type(original=False)
        self._original_entity_obj_type = self._check_obj_type(original=True)

        if self._entity_obj_type is None:
            self._entity_obj = None
        if self._original_entity_obj_type is None:
            self._original_entity_obj = None

        if self._check_for_changes_in_objects():
            print(f'{NOTIFIER_HEADER}\n{self._notify_string}')

        return None

    def _check_obj_type(self, original: bool) -> str:
        """
        Check object's type
        :param original: in order to difference between original and checked object
        :return: string represents object's type
        """
        if original:
            return self._check_type_from_entity_types_list(self._original_entity_obj)

        else:
            return self._check_type_from_entity_types_list(self._entity_obj)

    @staticmethod
    def _check_type_from_entity_types_list(obj: Any) -> Optional[str]:
        """
        Check if object's type is listed in ENTITY_TYPES
        :param obj:
        :return: The type from the list in case it was found, else, empty quotes if type was not found
        """
        if obj.__class__.__name__ in ENTITY_TYPES:
            return obj.__class__.__name__

        return None

    def _check_for_changes_in_objects(self) -> bool:
        """
        Check for changes in objects according to given constrains
        :return: True if there was any change, else False
        """
        if (self._original_entity_obj_type or self._entity_obj_type) == COMPANY:
            if self._check_changes_for_company():
                return True

        if (self._original_entity_obj_type or self._entity_obj_type) == EVENT or \
                (self._original_entity_obj_type or self._entity_obj_type) == WEBINAR or \
                (self._original_entity_obj_type or self._entity_obj_type) == CONTENT_ITEM:
            if self._check_changes_for_event_webinar_content():
                return True

        if (self._original_entity_obj_type or self._entity_obj_type) == COMPANY_FOR_EVENT or \
                (self._original_entity_obj_type or self._entity_obj_type) == COMPANY_FOR_WEBINAR:
            if self._check_changes_for_companyforevent_companyforwebinar():
                return True

        if (self._original_entity_obj_type or self._entity_obj_type) == COMPANY_COMPETITOR:
            if self._check_changes_for_companycompetitor():
                return True

        return False

    def _check_changes_for_company(self) -> bool:
        """
        Notify if either:
        -	New object
        -	Object is now physically deleted
        -	“is_deleted” attribute has changed (boolean, from true to false or vice-versa)
        -	“crawling_status” attribute has changed and is now one of TEXT_ANALYZED, TEXT_UPLOADED

        :return: True if one of the constraints was found
        """
        constrains = [
            self._is_new_entity_obj(),
            self._is_physically_deleted_entity_obj(),
            self._is_deleted_status_changed_within_obj(),
            self._is_crawling_status_changed()
        ]

        if constrains.count(True) > 0:
            return True

        return False

    def _check_changes_for_event_webinar_content(self) -> bool:
        """
        Notify if either:
        -	New object
        -	Object is now physically deleted
        -	“is_deleted” attribute has changed (boolean, from true to false or vice-versa)
        -	“is_blacklisted” attribute has changed (boolean, from true to false or vice-versa)
        -	“crawling_status” attribute has changed and is now one of TEXT_ANALYZED, TEXT_UPLOADED

        :return: True if one of the constraints was found
        """
        constrains = [
            self._is_new_entity_obj(),
            self._is_physically_deleted_entity_obj(),
            self._is_deleted_status_changed_within_obj(),
            self._is_blacklisted_status_changed_within_obj(),
            self._is_crawling_status_changed()
        ]

        if constrains.count(True) > 0:
            return True

        return False

    def _check_changes_for_companyforevent_companyforwebinar(self) -> bool:
        """
        Notify if either:
        -	New object
        -	Object is now physically deleted
        -	“is_deleted” attribute has changed (boolean, from true to false or vice-versa)
        -	“is_blacklisted” attribute has changed (boolean, from true to false or vice-versa)

        :return: True if one of the constraints was found
        """
        constrains = [
            self._is_new_entity_obj(),
            self._is_physically_deleted_entity_obj(),
            self._is_deleted_status_changed_within_obj(),
            self._is_blacklisted_status_changed_within_obj(),
        ]

        if constrains.count(True) > 0:
            return True

        return False

    def _check_changes_for_companycompetitor(self) -> bool:
        """
        Notify if either:
        -	New object
        -	Object is now physically deleted
        -	“is_deleted” attribute has changed (boolean, from true to false or vice-versa)

        :return: True if one of the constraints was found
        """
        constrains = [
            self._is_new_entity_obj(),
            self._is_physically_deleted_entity_obj(),
            self._is_deleted_status_changed_within_obj(),
        ]

        if constrains.count(True) > 0:
            return True

        return False

    def _is_new_entity_obj(self) -> bool:
        """
        Check if there is a new entity object and reformat notify string
        :returns: True if entity_obj is not None, in other cases returns False
        """
        if self._entity_obj is not None and self._original_entity_obj is None:
            self._notify_string += NOTIFY_MSG.format(
                object_type=self._entity_obj_type,
                reason=NEW_OBJ_REASON
            ) + '\n'
            return True

        return False

    def _is_physically_deleted_entity_obj(self) -> bool:
        """
        Check if original entity was deleted and reformat notify string
        :returns:
            True if original_entity_obj is not None, in other cases returns False
        """
        if self._entity_obj is None and self._original_entity_obj is not None:
            self._notify_string += NOTIFY_MSG.format(
                object_type=self._entity_obj_type,
                reason=PHYSICALLY_DELETE_REASON
            ) + '\n'
            return True

        return False

    def _is_deleted_status_changed_within_obj(self) -> bool:
        """
        Check  if is_deleted flag changed and reformat notify string
        :returns:
            True if original_entity_obj.is_deleted and entity_obj.is_deleted are NOT equals
            False if original_entity_obj.is_deleted and entity_obj.is_deleted are equals
        """
        if self._entity_obj is None or self._original_entity_obj is None:
            return False

        if self._original_entity_obj.is_deleted != self._entity_obj.is_deleted:
            self._notify_string += NOTIFY_MSG.format(
                object_type=self._entity_obj_type,
                reason=IS_DELETED_REASON
            ) + '\n'
            return True

        return False

    def _is_blacklisted_status_changed_within_obj(self) -> bool:
        """
        Check if is_blacklisted flag changed and reformat notify string
        :return:
            True if entity_obj.is_blacklisted set to True
            False if entity_obj.is_blacklisted set to False
        """
        if self._entity_obj is None or self._original_entity_obj is None:
            return False

        if self._entity_obj.is_blacklisted != self._original_entity_obj.is_blacklisted:
            self._notify_string += NOTIFY_MSG.format(
                object_type=self._entity_obj_type,
                reason=IS_BLACKLIST_REASON
            ) + '\n'
            return True

        return False

    def _is_crawling_status_changed(self) -> bool:
        """
        Check if crawling status changed to TEXT_ANALYZED or TEXT_UPLOADED and reformat notify string
        :return:
            True if crawling status changed, in other cases returns False
        """
        if self._entity_obj is None or self._original_entity_obj is None:
            return False

        if self._original_entity_obj.last_crawled != self._entity_obj.last_crawled:
            if self._entity_obj.last_crawled == CRAWLING_STATUSES.TEXT_ANALYZED or \
                    self._entity_obj.last_crawled == CRAWLING_STATUSES.TEXT_UPLOADED:
                self._notify_string += NOTIFY_MSG.format(
                    object_type=self._entity_obj_type,
                    reason=CRAWLING_STATUS_REASON
                ) + '\n'
                return True

        return False

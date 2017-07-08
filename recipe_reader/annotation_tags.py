#!/usr/bin/env python3
"""Reader classes that serve as interfaces for the annotation tags in the 
annotated recipe documents.
"""
class Tag:
    def __init__(self, tag):
        """Initialize a Tag object.

        tag -- a BeautifulSoup tag object 
        """
        self.name = tag.name
        self.id = tag["id"]

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

class ExtentTag(Tag):
    def __init__(self, tag):
        super(ExtentTag, self).__init__(tag)
        # split the string "xx~xx" into two parts, and convert 
        # each part into an integer.
        self.start, self.end = map(int, tag["spans"].split("~"))
        self.text = tag["text"]

    def get_range(self):
        return self.start, self.end

    def get_text(self):
        return self.text

    def contains_index(self, index):
        """Returns true if the given index is within the range of this tag.
        """
        return index >= self.start and index < self.end

class LinkTag(Tag):
    def __init__(self, tag):
        super(LinkTag, self).__init__(tag)
        self.first_id = None
        self.first_text = None
        self.second_id = None
        self.second_id = None

class ActionTag(ExtentTag):
    def __init__(self, tag):
        super(ActionTag, self).__init__(tag)
        self.act_type = tag["act_type"]

    def get_action_type(self):
        return self.act_type

class IngredientTag(ExtentTag):
    def __init__(self, tag):
        super(IngredientTag, self).__init__(tag)
        self.start_state = tag["start_state"]
        self.composite = tag["composite"]

    def is_start_state(self):
        return self.start_state

    def is_composite(self):
        return self.composite

class ToolTag(ExtentTag):
    def __init__(self, tag):
        super(ToolTag, self).__init__(tag)

class QuantityTag(ExtentTag):
    def __init__(self, tag):
        super(QuantityTag, self).__init__(tag)

class UnitTag(ExtentTag):
    def __init__(self, tag):
        super(UnitTag, self).__init__(tag)

class FlowTag(LinkTag):
    def __init__(self, tag):
        super(FlowTag, self).__init__(tag)
        self.first_id = tag["fromID"]
        self.first_text = tag["fromText"]
        self.second_id = tag["toID"]
        self.second_text = tag["toText"]

    def get_from_id(self):
        return self.first_id

    def get_from_text(self):
        return self.first_text

    def get_to_id(self):
        return self.second_id

    def get_to_text(self):
        return self.second_text

class CorefTag(LinkTag):
    def __init__(self, tag):
        super(CorefTag, self).__init__(tag)
        self.first_id = tag["exp_aID"]
        self.first_text = tag["exp_aText"]
        self.second_id = tag["exp_bID"]
        self.second_text = tag["exp_bText"]

    def get_exp_a_id(self):
        return self.first_id

    def get_exp_a_text(self):
        return self.first_text

    def get_exp_b_id(self):
        return self.second_id
    
    def get_exp_b_text(self):
        return self.second_text

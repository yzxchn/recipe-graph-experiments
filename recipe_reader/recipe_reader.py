from bs4 import BeautifulSoup
from .annotation_tags import *

class AnnotatedRecipe:
    """A reader for the annotated recipes saved in XML.
    """
    TAG_ACTION = "Action"
    TAG_INGREDIENT = "Ingredient"
    TAG_QUANTITY = "Quantity"
    TAG_UNIT = "Unit"
    TAG_TOOL = "Tool"
    TAG_FLOW = "Flow"
    TAG_COREF = "Coref"
    EXTENT_TAGS = {TAG_ACTION, TAG_INGREDIENT, TAG_QUANTITY, TAG_UNIT, TAG_TOOL}
    LINK_TAGS = {TAG_FLOW, TAG_COREF}
    TAG_NAME_MAP = {"Action":ActionTag, "Ingredient":IngredientTag, 
                    "Tool":ToolTag, "Unit":UnitTag, 
                    "Quantity":QuantityTag, "Flow":FlowTag, 
                    "Coref":CorefTag}

    def __init__(self, path):
        with open(path) as f:
            self.soup = BeautifulSoup(f,"xml")
        self.text = self.soup.TEXT.get_text()
        self.sections = self.text.split("\n\n")
        self._find_starting_indexes()
        self._find_tags()

    def _find_starting_indexes(self):
        """Determines the starting indexes of each section (title, time, 
        ingredients and instructions) in the whole recipe.
        """
        self.title_beg = 0
        self.time_beg = self.text.index("\n\n", self.title_beg)+2
        self.ingredients_beg = self.text.index("\n\n", self.time_beg)+2
        self.instructions_beg = self.text.index("\n\n", 
                                                    self.ingredients_beg)+2

    def _find_tags(self):
        """Finds the extent and link tags provided in the annotated recipe.
        """
        self.tags = []
        self.extent_tags = []
        self.link_tags = []
        for t in self.soup.TAGS.contents:
            if t != "\n" and t.name in AnnotatedRecipe.EXTENT_TAGS:
                et = AnnotatedRecipe.TAG_NAME_MAP[t.name](t)
                self.tags.append(et)
                self.extent_tags.append(et)
            elif t != "\n" and t.name in AnnotatedRecipe.LINK_TAGS:
                lt = AnnotatedRecipe.TAG_NAME_MAP[t.name](t)
                self.tags.append(lt)
                self.link_tags.append(lt)

    def get_name(self):
        return self.sections[0]

    def get_time(self):
        return self.sections[1]

    def get_ingredients(self):
        return self.sections[2]

    def get_instructions(self):
        return self.sections[3]

    def get_tags(self):
        return self.tags

    def get_extent_tags(self):
        return self.extent_tags

    def get_link_tags(self):
        return self.link_tags

    def get_covering_entities(self, beg, end):
        """Given a range of index in document, find the entity(s) 
        that covers this range. A range is covered if the beginning 
        index of the range is within the range of an entity.

        beg - begging of the range index to be searched in the document
        end - end of the range to be searched in the document.
        """
        covering_tags = []
        for ext_tag in self.extent_tags:
            if ext_tag.contains_index(beg):
                covering_tags.append(ext_tag.get_id())
        return covering_tags

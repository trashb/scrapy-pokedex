import scrapy
from ..items import PokedexItem

#solution to not being able to import inputted pkmn from main :,)
f = open("pkmn.txt","r")
pkmn = f.read()
f.close()


class PokedexSpider(scrapy.Spider):
    name = "pokedex"            #spider name
    allowed_domains = ["pokemondb.net"]     #make sure spider stays in this domain
    start_urls = ["https://pokemondb.net/pokedex/"+ pkmn]   #will scrape the link of the inputted pkmn
    item = PokedexItem()        #dict in items.py

######################################## DATA DICT ########################################
#data and where to find them (see first few lines of parse function)
    pokedex_data = {
        "a_national": "tr:nth-child(1) strong::text", 
        "b_types": "tr:nth-child(2) a::text", 
        "c_species": "tr:nth-child(3) td::text",
        "d_height": "tr:nth-child(4) td::text",
        "e_weight": "tr:nth-child(5) td::text",
        "f_abilities": "tr:nth-child(6) span a::text",
    }

    breeding_data = {
        "g_groups": "tr:nth-child(1) a::text",
        "h_gender": "tr:nth-child(2) span::text", #can be empty (if genderless)
        "i_cycles": "tr:nth-child(3) td::text" 
    }

    effect_data = {
        "j_weakness": "td",     
        "k_resistance": "td",   #can be empty
        "l_immune": "td"        #can be empty
    }

######################################## PARSE ########################################

    def parse(self, response):
        #get where to find items above
        pokedex_table = response.css(".active .text-center+ .span-lg-4 table.vitals-table tbody")
                        #in active class, after text-center class, in span-lg-4 class, in table with class, in table body
        breeding_table = response.css(".active .span-lg-12+ .span-lg-12 table.vitals-table tbody")
        effect_table = response.css(".sv-tabs-panel.active .grid-row+ .grid-row .span-lg-4 .text-center .type-table-pokedex tr+ tr")

        #loop through each key in dict and extract the data using the value (which indicates location in html)
        #then put extracted data in corresponding key[val] location in items dict (from items.py)           
        for key, val in self.pokedex_data.items():
            self.item[key] = pokedex_table.css(val).extract()
        for key, val in self.breeding_data.items():
            self.item[key] = breeding_table.css(val).extract()

        for key, val in self.effect_data.items():
            output = []     #will contain all types that are super/not very/ineffective

            #get the title tag (<title>) of all types
            types = []
            for i in range(0, len(effect_table.css(val))):  #for each td (one pkmn type per td):
                types.append(effect_table.css(val)[i].attrib["title"])  #extract title
                #title ex: "Normal → Water/Flying = normal effectiveness"
                abbr = types[i][0:3]    #abbreviation (just the first 3 letters is enough; easier on the eyes)
                #put types in their correct category and check fo duplicates (may occur due to layout of website)
                if key=="j_weakness" and "super" in types[i] and abbr not in output:
                    output.append(abbr)        
                elif key=="k_resistance" and "not" in types[i] and abbr not in output:
                    output.append(abbr)
                elif  key=="l_immune" and "no " in types[i] and abbr not in output:
                    output.append(abbr)

            self.item[key] = output #set list of pokemon types for the respective key

        #return items dict (from items.py) with all the info filled
        yield self.item

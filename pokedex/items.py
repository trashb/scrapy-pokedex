# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PokedexItem(scrapy.Item):
    # define the fields for your item here

    #abcd etc. added to keep info in this order 
    #standard stuff
    a_national = scrapy.Field()   #national pokedex number (includes pkmn from all regions)
    b_types = scrapy.Field()      
    c_species = scrapy.Field()    
    d_height = scrapy.Field()
    e_weight = scrapy.Field()
    f_abilities = scrapy.Field()  #provide passive effects in battle/overworld

    #pokemon breeding-related
    g_groups = scrapy.Field()     #egg groups (pkmn of the same egg groups can breed)
    h_gender = scrapy.Field()     #gender ratios (eg. some pkmn are more likely to be male than female)
    i_cycles = scrapy.Field()     #how many steps egg takes to hatch

    #pokemon type advantages/disadvantages
    j_weakness = scrapy.Field()       #type is super-effective (does more dmg)
    k_resistance = scrapy.Field()     #type is not really effective (does less dmg)
    l_immune = scrapy.Field()         #type is ineffective (does no dmg)




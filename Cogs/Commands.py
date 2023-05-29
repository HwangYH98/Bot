from discord import app_commands
from discord.ext import commands
from discord import Interaction, SelectOption, app_commands, Object
from discord.ui import Button, View, Select, Modal, TextInput
import discord
import csv
from run_selenium import efreshData_csv
import threading

class server_Certified_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.thread = False

    def command_search_restaurants(self, keyword, budget):
        restaurant_list = []
        restaurant_title_list = []

        with open('stores.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        for row in rows:
            try:
                if row[1] == keyword:
                    if int(row[7]) == 0 and int(row[8]) == 0 and int(row[9]) == 0:
                        pass
                    else:
                        if int(row[7]) == int(row[8]) and int(row[7]) <= int(budget):
                            if row[0] not in restaurant_title_list:
                                restaurant_list.append(row)
                                restaurant_title_list.append(row[0])
                        else:
                            if int(row[9]) <= int(budget):
                                if row[0] not in restaurant_title_list:
                                    restaurant_list.append(row)
                                    restaurant_title_list.append(row[0])
            except:
                pass

        return restaurant_list
    
    def command_search_ages(self, keyword, budget):
        restaurant_list = []
        restaurant_title_list = []

        with open('stores.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        for row in rows:
            try:
                if keyword in row[13]:
                    if int(row[7]) == 0 and int(row[8]) == 0 and int(row[9]) == 0:
                        pass
                    else:
                        if int(row[7]) == int(row[8]) and int(row[7]) <= int(budget): 
                            if row[0] not in restaurant_title_list:
                                restaurant_list.append(row)
                                restaurant_title_list.append(row[0])
                        else:
                            if int(row[9]) <= int(budget):
                                if row[0] not in restaurant_title_list:
                                    restaurant_list.append(row)
                                    restaurant_title_list.append(row[0])
            except:
                pass

        return restaurant_list
    
    def command_search_purposes(self, keyword, budget):
        restaurant_list = []
        restaurant_title_list = []

        with open('stores.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        for row in rows:
            try:
                if keyword in row[14]:
                    if int(row[7]) == 0 and int(row[8]) == 0 and int(row[9]) == 0:
                        pass
                    else:
                        if int(row[7]) == int(row[8]) and int(row[7]) <= int(budget):
                            if row[0] not in restaurant_title_list:
                                restaurant_list.append(row)
                                restaurant_title_list.append(row[0])
                        else:
                            if int(row[9]) <= int(budget):
                                if row[0] not in restaurant_title_list:
                                    restaurant_list.append(row)
                                    restaurant_title_list.append(row[0])
            except:
                pass

        return restaurant_list
    
    def command_search_moods(self, keyword, budget):
        restaurant_list = []
        restaurant_title_list = []
        with open('stores.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        for row in rows:
            try:
                if keyword in row[15]:
                    if int(row[7]) == 0 and int(row[8]) == 0 and int(row[9]) == 0:
                        pass
                    else:
                        if int(row[7]) == int(row[8]) and int(row[7]) <= int(budget):
                            if row[0] not in restaurant_title_list:
                                restaurant_list.append(row)
                                restaurant_title_list.append(row[0])
                        else:
                            if int(row[9]) <= int(budget):
                                if row[0] not in restaurant_title_list:
                                    restaurant_list.append(row)
                                    restaurant_title_list.append(row[0])
            except:
                pass

        return restaurant_list
    
    def make_embeds(slef, restaurant_list):
        embed_list = []

        for restaurant in restaurant_list:
            embed = discord.Embed(title=f"{restaurant[0]}", color=0x62c1cc)
            replaced_address = restaurant[2].replace(" ", "%20")
            Address = 'https://map.naver.com/v5/search/'+replaced_address
            embed.add_field(name= "🏠 주소", value = "[{0}](<{1}>)".format(restaurant[2], Address), inline = False)

            if restaurant[3] == '':
                embed.add_field(name= "☎️ 전화번호", value = "게시되지 않음", inline = False)
            else:
                embed.add_field(name= "☎️ 전화번호", value = f"{restaurant[3]}", inline = False)

            if restaurant[4] == "게시되지 않음 None":
                embed.add_field(name= "⌛ 영업시간", value = "게시되지 않음", inline = False)
            else:
                embed.add_field(name= "⌛ 영업시간", value = f"{restaurant[4]}", inline = False)

            embed.add_field(name= "🍚 메뉴", value = "", inline = False)

            if restaurant[11] == "게시되지 않음":
                pass
            else:
                embed.set_thumbnail(url=restaurant[11])

            prices = eval(restaurant[6])

            for i, munu in enumerate(eval(restaurant[5])):
                if i == 15:
                    
                    embed.add_field(name= "", value = f"그 외 {len(eval(restaurant[5]))-15}개 더..", inline = False)
                elif i < 15:
                    embed.add_field(name= "", value = f"{munu} ({prices[i]})", inline = False)

            embed.add_field(name= "평점",value = f"{restaurant[10]}", inline = False)
            embed.add_field(name= "",value = "[{0}](<{1}>)".format("바로가기", restaurant[12]), inline = False)

            embed_list.append(embed)
        return embed_list
    
    def format_currency(self, amount):
        try:
            amount = int(amount)
            formatted_amount = "{:,.0f}".format(amount)
            return formatted_amount
        except ValueError:
            return "Invalid input"
    
    async def command_create_more_button(self, interaction:discord.Interaction, embeds):
        create_more_button = Button(label="더보기", style = discord.ButtonStyle.blurple)

        async def ages_button_Progress_callback(interaction:discord.Interaction):
            await self.command_create_more_button(interaction, embeds[5:])

        create_more_button.callback = ages_button_Progress_callback
        view = View(timeout=None)
        view.add_item(create_more_button)
        
        if len(embeds) > 5:
            await interaction.response.send_message(embeds=embeds[:5], view=view, ephemeral=True)
        else:
            await interaction.response.send_message(embeds=embeds[:5], ephemeral=True)

    async def caht_bot(self, interaction, budget):
        selects_button_1 = Button(label="이용자층별", style = discord.ButtonStyle.blurple)
        selects_button_2 = Button(label="카테고리별", style = discord.ButtonStyle.blurple)
        selects_button_3 = Button(label="목적별", style = discord.ButtonStyle.blurple)
        selects_button_4 = Button(label="분위기별", style = discord.ButtonStyle.blurple)

        async def selects_button_1_callback(interaction:discord.Interaction):
            ages_button_1 = Button(label="20대", style = discord.ButtonStyle.blurple)
            ages_button_2 = Button(label="30대", style = discord.ButtonStyle.blurple)
            ages_button_3 = Button(label="40대", style = discord.ButtonStyle.blurple)
            ages_button_4 = Button(label="50대", style = discord.ButtonStyle.blurple)
            ages_button_5 = Button(label="60대이상", style = discord.ButtonStyle.blurple)
            ages_button_6 = Button(label="뒤로가기", style = discord.ButtonStyle.red)
     
            async def ages_button_Progress_callback(interaction:discord.Interaction, ver):
                restaurant_list = self.command_search_ages(ver, budget)
                if restaurant_list:
                    embeds = self.make_embeds(restaurant_list)
                    await self.command_create_more_button(interaction, embeds)
                else:
                    await interaction.response.send_message("조건에 충족하는 결과가 없습니다.")

            async def ages_button_cancel_callback(interaction:discord.Interaction):
                await self.caht_bot(interaction, budget)

            ages_button_1.callback = lambda i: ages_button_Progress_callback(i, "20대")
            ages_button_2.callback = lambda i: ages_button_Progress_callback(i, "30대")
            ages_button_3.callback = lambda i: ages_button_Progress_callback(i, "40대")
            ages_button_4.callback = lambda i: ages_button_Progress_callback(i, "50대")
            ages_button_5.callback = lambda i: ages_button_Progress_callback(i, "60대%20이상")
            ages_button_6.callback = ages_button_cancel_callback

            view = View(timeout=None)
            view.add_item(ages_button_1)
            view.add_item(ages_button_2)
            view.add_item(ages_button_3)
            view.add_item(ages_button_4)
            view.add_item(ages_button_5)
            view.add_item(ages_button_6)
            
            log_embed = discord.Embed(title="💬 검색을 원하시는 카테고리를 선택해주세요", color=0x62c1cc)
            log_embed.add_field(name= "", value = f"선택하신 가격대 {self.format_currency(budget)}", inline = False)
            await interaction.response.send_message(embed=log_embed, view=view, ephemeral=True)

        async def selects_button_2_callback(interaction:discord.Interaction):
            Categories_button_1 = Button(label="배달", style = discord.ButtonStyle.blurple)
            Categories_button_2 = Button(label="밥집", style = discord.ButtonStyle.blurple)
            Categories_button_3 = Button(label="카페", style = discord.ButtonStyle.blurple)
            Categories_button_4 = Button(label="술집", style = discord.ButtonStyle.blurple)
            Categories_button_5 = Button(label="고깃집", style = discord.ButtonStyle.blurple)
            Categories_button_6 = Button(label="횟집", style = discord.ButtonStyle.blurple)
            Categories_button_7 = Button(label="한식", style = discord.ButtonStyle.blurple)
            Categories_button_8 = Button(label="중식", style = discord.ButtonStyle.blurple)
            Categories_button_9 = Button(label="일식", style = discord.ButtonStyle.blurple)
            Categories_button_10 = Button(label="양식", style = discord.ButtonStyle.blurple)
            Categories_button_11 = Button(label="아시안", style = discord.ButtonStyle.blurple)
            Categories_button_12 = Button(label="멕시칸", style = discord.ButtonStyle.blurple)
            Categories_button_13 = Button(label="이탈리안", style = discord.ButtonStyle.blurple)
            Categories_button_14 = Button(label="뷔폐", style = discord.ButtonStyle.blurple)
            Categories_button_15 = Button(label="브런치", style = discord.ButtonStyle.blurple)
            Categories_button_16 = Button(label="패스트푸드", style = discord.ButtonStyle.blurple)
            Categories_button_17 = Button(label="분식", style = discord.ButtonStyle.blurple)
            Categories_button_18 = Button(label="국물요리", style = discord.ButtonStyle.blurple)
            Categories_button_19 = Button(label="면요리", style = discord.ButtonStyle.blurple)
            Categories_button_20 = Button(label="해산물", style = discord.ButtonStyle.blurple)
            Categories_button_21 = Button(label="뒤로가기", style = discord.ButtonStyle.red)
                 
            async def Categories_button_Progress_callback(interaction:discord.Interaction, ver):
                restaurant_list = self.command_search_restaurants(ver, budget)
                if restaurant_list:
                    embeds = self.make_embeds(restaurant_list)
                    await self.command_create_more_button(interaction, embeds)
                else:
                    await interaction.response.send_message("조건에 충족하는 결과가 없습니다.")

            async def Categories_button_cancel_callback(interaction:discord.Interaction):
                await self.caht_bot(interaction, budget)

            Categories_button_1.callback = lambda i: Categories_button_Progress_callback(i, "배달")
            Categories_button_2.callback = lambda i: Categories_button_Progress_callback(i, "밥집")
            Categories_button_3.callback = lambda i: Categories_button_Progress_callback(i, "카페")
            Categories_button_4.callback = lambda i: Categories_button_Progress_callback(i, "술집")
            Categories_button_5.callback = lambda i: Categories_button_Progress_callback(i, "고깃집")
            Categories_button_6.callback = lambda i: Categories_button_Progress_callback(i, "횟집")
            Categories_button_7.callback = lambda i: Categories_button_Progress_callback(i, "한식")
            Categories_button_8.callback = lambda i: Categories_button_Progress_callback(i, "중식")
            Categories_button_9.callback = lambda i: Categories_button_Progress_callback(i, "일식")
            Categories_button_10.callback = lambda i: Categories_button_Progress_callback(i, "양식")
            Categories_button_11.callback = lambda i: Categories_button_Progress_callback(i, "아시안")
            Categories_button_12.callback = lambda i: Categories_button_Progress_callback(i, "멕시칸")
            Categories_button_13.callback = lambda i: Categories_button_Progress_callback(i, "이탈리안")
            Categories_button_14.callback = lambda i: Categories_button_Progress_callback(i, "뷔폐")
            Categories_button_15.callback = lambda i: Categories_button_Progress_callback(i, "브런치")
            Categories_button_16.callback = lambda i: Categories_button_Progress_callback(i, "패스트푸드")
            Categories_button_17.callback = lambda i: Categories_button_Progress_callback(i, "분식")
            Categories_button_18.callback = lambda i: Categories_button_Progress_callback(i, "국물요리")
            Categories_button_19.callback = lambda i: Categories_button_Progress_callback(i, "면요리")
            Categories_button_20.callback = lambda i: Categories_button_Progress_callback(i, "해산물")
            Categories_button_21.callback = Categories_button_cancel_callback

            view = View(timeout=None)
            view.add_item(Categories_button_1)
            view.add_item(Categories_button_2)
            view.add_item(Categories_button_3)
            view.add_item(Categories_button_4)
            view.add_item(Categories_button_5)
            view.add_item(Categories_button_6)
            view.add_item(Categories_button_7)
            view.add_item(Categories_button_8)
            view.add_item(Categories_button_9)
            view.add_item(Categories_button_10)
            view.add_item(Categories_button_11)
            view.add_item(Categories_button_12)
            view.add_item(Categories_button_13)
            view.add_item(Categories_button_14)
            view.add_item(Categories_button_15)
            view.add_item(Categories_button_16)
            view.add_item(Categories_button_17)
            view.add_item(Categories_button_18)
            view.add_item(Categories_button_19)
            view.add_item(Categories_button_20)
            view.add_item(Categories_button_21)

            log_embed = discord.Embed(title="💬 검색을 원하시는 카테고리를 선택해주세요", color=0x62c1cc)
            log_embed.add_field(name= "", value = f"선택하신 가격대 {self.format_currency(budget)}", inline = False)
            await interaction.response.send_message(embed=log_embed, view=view, ephemeral=True)

        async def selects_button_3_callback(interaction:discord.Interaction):
            purposes_button_1 = Button(label="아침식사", style = discord.ButtonStyle.blurple)
            purposes_button_2 = Button(label="점식식사", style = discord.ButtonStyle.blurple)
            purposes_button_3 = Button(label="저녁식사", style = discord.ButtonStyle.blurple)
            purposes_button_4 = Button(label="혼밥", style = discord.ButtonStyle.blurple)
            purposes_button_5 = Button(label="혼술", style = discord.ButtonStyle.blurple)
            purposes_button_6 = Button(label="혼카페", style = discord.ButtonStyle.blurple)
            purposes_button_7 = Button(label="데이트", style = discord.ButtonStyle.blurple)
            purposes_button_8 = Button(label="회식", style = discord.ButtonStyle.blurple)
            purposes_button_9 = Button(label="건강식", style = discord.ButtonStyle.blurple)
            purposes_button_10 = Button(label="다이어트", style = discord.ButtonStyle.blurple)
            purposes_button_11 = Button(label="가족외식", style = discord.ButtonStyle.blurple)
            purposes_button_12 = Button(label="아이동반", style = discord.ButtonStyle.blurple)
            purposes_button_13 = Button(label="실버푸드", style = discord.ButtonStyle.blurple)
            purposes_button_14 = Button(label="식사모임", style = discord.ButtonStyle.blurple)
            purposes_button_15 = Button(label="술모임", style = discord.ButtonStyle.blurple)
            purposes_button_16 = Button(label="차모임", style = discord.ButtonStyle.blurple)
            purposes_button_17 = Button(label="접대", style = discord.ButtonStyle.blurple)
            purposes_button_18 = Button(label="간식", style = discord.ButtonStyle.blurple)
            purposes_button_19 = Button(label="뒤로가기", style = discord.ButtonStyle.red)

            async def purposes_button_Progress_callback(interaction:discord.Interaction, ver):
                restaurant_list = self.command_search_purposes(ver, budget)
                if restaurant_list:
                    embeds = self.make_embeds(restaurant_list)
                    await self.command_create_more_button(interaction, embeds)
                else:
                    await interaction.response.send_message("조건에 충족하는 결과가 없습니다.")

            async def purposes_button_cancel_callback(interaction:discord.Interaction):
                await self.caht_bot(interaction, budget)

            purposes_button_1.callback = lambda i: purposes_button_Progress_callback(i, "아침식사")
            purposes_button_2.callback = lambda i: purposes_button_Progress_callback(i, "점식식사")
            purposes_button_3.callback = lambda i: purposes_button_Progress_callback(i, "저녁식사")
            purposes_button_4.callback = lambda i: purposes_button_Progress_callback(i, "혼밥")
            purposes_button_5.callback = lambda i: purposes_button_Progress_callback(i, "혼술")
            purposes_button_6.callback = lambda i: purposes_button_Progress_callback(i, "혼카페")
            purposes_button_7.callback = lambda i: purposes_button_Progress_callback(i, "데이트")
            purposes_button_8.callback = lambda i: purposes_button_Progress_callback(i, "회식")
            purposes_button_9.callback = lambda i: purposes_button_Progress_callback(i, "건강식")
            purposes_button_10.callback = lambda i: purposes_button_Progress_callback(i, "다이어트")
            purposes_button_11.callback = lambda i: purposes_button_Progress_callback(i, "가족외식")
            purposes_button_12.callback = lambda i: purposes_button_Progress_callback(i, "아이동반")
            purposes_button_13.callback = lambda i: purposes_button_Progress_callback(i, "실버푸드")
            purposes_button_14.callback = lambda i: purposes_button_Progress_callback(i, "식사모임")
            purposes_button_15.callback = lambda i: purposes_button_Progress_callback(i, "술모임")
            purposes_button_16.callback = lambda i: purposes_button_Progress_callback(i, "차모임")
            purposes_button_17.callback = lambda i: purposes_button_Progress_callback(i, "접대")
            purposes_button_18.callback = lambda i: purposes_button_Progress_callback(i, "간식")
            purposes_button_19.callback = purposes_button_cancel_callback

            view = View(timeout=None)
            view.add_item(purposes_button_1)
            view.add_item(purposes_button_2)
            view.add_item(purposes_button_3)
            view.add_item(purposes_button_4)
            view.add_item(purposes_button_5)
            view.add_item(purposes_button_6)
            view.add_item(purposes_button_7)
            view.add_item(purposes_button_8)
            view.add_item(purposes_button_9)
            view.add_item(purposes_button_10)
            view.add_item(purposes_button_11)
            view.add_item(purposes_button_12)
            view.add_item(purposes_button_13)
            view.add_item(purposes_button_14)
            view.add_item(purposes_button_15)
            view.add_item(purposes_button_16)
            view.add_item(purposes_button_17)
            view.add_item(purposes_button_18)
            view.add_item(purposes_button_19)

            log_embed = discord.Embed(title="💬 검색을 원하시는 목적을 선택해주세요", color=0x62c1cc)
            log_embed.add_field(name= "", value = f"선택하신 가격대 {self.format_currency(budget)}", inline = False)
            await interaction.response.send_message(embed=log_embed, view=view, ephemeral=True)

        async def selects_button_4_callback(interaction:discord.Interaction):
            moods_button_1 = Button(label="가성비좋은", style = discord.ButtonStyle.blurple)
            moods_button_2 = Button(label="분위기좋은", style = discord.ButtonStyle.blurple)
            moods_button_3 = Button(label="푸짐한", style = discord.ButtonStyle.blurple)
            moods_button_4 = Button(label="격식있는", style = discord.ButtonStyle.blurple)
            moods_button_5 = Button(label="고급스러운", style = discord.ButtonStyle.blurple)
            moods_button_6 = Button(label="서민적인", style = discord.ButtonStyle.blurple)
            moods_button_7 = Button(label="시끌벅적한", style = discord.ButtonStyle.blurple)
            moods_button_8 = Button(label="조용한", style = discord.ButtonStyle.blurple)
            moods_button_9 = Button(label="깔끔한", style = discord.ButtonStyle.blurple)
            moods_button_10 = Button(label="이색적인", style = discord.ButtonStyle.blurple)
            moods_button_11 = Button(label="뷰가좋은", style = discord.ButtonStyle.blurple)
            moods_button_12 = Button(label="예쁜", style = discord.ButtonStyle.blurple)
            moods_button_13 = Button(label="지역주민이찾는", style = discord.ButtonStyle.blurple)
            moods_button_14 = Button(label="뒤로가기", style = discord.ButtonStyle.red)

            async def moods_button_Progress_callback(interaction:discord.Interaction, ver):
                restaurant_list = self.command_search_moods(ver, budget)
                if restaurant_list:
                    embeds = self.make_embeds(restaurant_list)
                    await self.command_create_more_button(interaction, embeds)
                else:
                    await interaction.response.send_message("조건에 충족하는 결과가 없습니다.")

            async def moods_button_cancel_callback(interaction:discord.Interaction):
                await self.caht_bot(interaction, budget)

            moods_button_1.callback = lambda i: moods_button_Progress_callback(i, "가성비좋은")
            moods_button_2.callback = lambda i: moods_button_Progress_callback(i, "분위기좋은")
            moods_button_3.callback = lambda i: moods_button_Progress_callback(i, "푸짐한")
            moods_button_4.callback = lambda i: moods_button_Progress_callback(i, "격식있는")
            moods_button_5.callback = lambda i: moods_button_Progress_callback(i, "고급스러운")
            moods_button_6.callback = lambda i: moods_button_Progress_callback(i, "서민적인")
            moods_button_7.callback = lambda i: moods_button_Progress_callback(i, "시끌벅적한")
            moods_button_8.callback = lambda i: moods_button_Progress_callback(i, "조용한")
            moods_button_9.callback = lambda i: moods_button_Progress_callback(i, "깔끔한")
            moods_button_10.callback = lambda i: moods_button_Progress_callback(i, "이색적인")
            moods_button_11.callback = lambda i: moods_button_Progress_callback(i, "뷰가좋은")
            moods_button_12.callback = lambda i: moods_button_Progress_callback(i, "예쁜")
            moods_button_13.callback = lambda i: moods_button_Progress_callback(i, "지역주민이찾는")
            moods_button_14.callback = moods_button_cancel_callback

            view = View(timeout=None)
            view.add_item(moods_button_1)
            view.add_item(moods_button_2)
            view.add_item(moods_button_3)
            view.add_item(moods_button_4)
            view.add_item(moods_button_5)
            view.add_item(moods_button_6)
            view.add_item(moods_button_7)
            view.add_item(moods_button_8)
            view.add_item(moods_button_9)
            view.add_item(moods_button_10)
            view.add_item(moods_button_11)
            view.add_item(moods_button_12)
            view.add_item(moods_button_13)
            view.add_item(moods_button_14)

            log_embed = discord.Embed(title="💬 검색을 원하시는 분위기를 선택해주세요", color=0x62c1cc)
            log_embed.add_field(name= "", value = f"선택하신 가격대 {self.format_currency(budget)}", inline = False)
            await interaction.response.send_message(embed=log_embed, view=view, ephemeral=True)

        selects_button_1.callback = selects_button_1_callback
        selects_button_2.callback = selects_button_2_callback
        selects_button_3.callback = selects_button_3_callback
        selects_button_4.callback = selects_button_4_callback

        view = View(timeout=None)
        view.add_item(selects_button_1)
        view.add_item(selects_button_2)
        view.add_item(selects_button_3)
        view.add_item(selects_button_4)

        log_embed = discord.Embed(title="💬 검색을 원하시는 범주를 선택해주세요", color=0x62c1cc)
        log_embed.add_field(name= "", value = f"선택하신 가격대 {self.format_currency(budget)}", inline = False)
        await interaction.response.send_message(embed=log_embed, view=view, ephemeral=True)
        
    @app_commands.command(name="맛집검색")
    async def def_command_search_restaurants(self, interaction: Interaction, budget: int) -> None:
        if not hasattr(self, 'thread') or not (self.thread and self.thread.is_alive()):
            await self.caht_bot(interaction, budget)
        else:
            log_embed = discord.Embed(title="❌ 사용할 수 없음", color=0xc91616)
            log_embed.add_field(name= "", value = "현재 데이터를 채우는 중이므로 사용하실 수 없습니다.", inline = False)
            await interaction.response.send_message(embed=log_embed, ephemeral=True)
            
    @app_commands.command(name="데이터재검색")
    async def refreshData(self, interaction: Interaction) -> None:
        if interaction.guild.get_member(interaction.user.id).guild_permissions.ban_members:
            if not hasattr(self, 'thread') or not (self.thread and self.thread.is_alive()):
                log_embed = discord.Embed(title="🔎 데이터검색 중", color=0x62c1cc)
                log_embed.add_field(name= "", value = "데이터를 검색해 csv파일을 채웁니다.\n작업은 컴퓨터 환경에 따라 최소 20분정도 소요됩니다.", inline = False)   
                await interaction.response.send_message(embed=log_embed, ephemeral=True)
                self.thread = threading.Thread(target=efreshData_csv)
                self.thread.start()
            else:
                log_embed = discord.Embed(title="❌ 검색할 수 없음", color=0xc91616)
                log_embed.add_field(name= "", value = "이미 데이터를 검색 중이므로 명령어를 사용하실 수 없습니다.", inline = False)   
                await interaction.response.send_message(embed=log_embed, ephemeral=True)
        else:
            await interaction.response.send_message("권한이 없습니다.", ephemeral=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): 
            pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_Certified_cog(bot))

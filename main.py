import discord
from random import randint
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Activity, ActivityType
from discord import Embed
import asyncio
import datetime
import json

Bot = commands.Bot(command_prefix="$")
queue = []
bonus1 = []

#<==================================================================>
#Команды для фарма, и остального
#<==================================================================>

#$cmds - бонус 1000 карбованцівок передать.
@Bot.command()
async def cmds(ctx):
    emb1 = discord.Embed(title='cmds', color= discord.Color.green())
    emb1.add_field(name="Для администрации:", value='☀', inline= False )
    emb1.add_field(name="addrole @role *cost*", value='Добавить роль в магазин.', inline= False)
    emb1.add_field(name="delrole @role", value='Удалить роль из магазина.', inline= False)
    emb1.add_field(name="give *cost*", value='Выдать себе карбованці.', inline= False)
    emb1.add_field(name="say *text*", value='Сказать от лица бота.', inline= False)
    emb1.add_field(name="Для обычного пользователя:", value='☀', inline= False )
    emb1.add_field(name="shop", value='Просмотреть список доступных для покупки ролей в магазине.', inline= False)
    emb1.add_field(name="buy @role", value='Купить роль из магазина.', inline= False)
    emb1.add_field(name="who *text*", value='Случайным образом выбирает человека.', inline= False)
    emb1.add_field(name="pr *text*", value='Случайным образом выбирает процентное соотношение.', inline= False)
    emb1.add_field(name="coin", value='Случайным образом выбирает занчения: Орел, или решка.', inline= False)
    emb1.add_field(name="random *value1* *value2*", value='Случайным образом выбирает значения из заданых ему промежутков.', inline= False)
    emb1.add_field(name="timely", value='Получить карбованці. Доступно раз в 10 минут.', inline= False)
    emb1.add_field(name="bonus", value='Получить бонус в виде карбованців. Доступно раз в 24 часа', inline= False)
    emb1.add_field(name="casino *cost*", value='Казино. Случайным образом выберает значение. Может удвоить сумму, или она может пропасть.', inline= False)
    emb1.add_field(name="roulette *cost*", value='Рулетка. Нужно выбить три, или два одинаковых значения.', inline= False)
    emb1.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    await ctx.send (embed= emb1)



#$timely - бонус 1000 карбованцівок передать.
@Bot.command()
@commands.has_permissions(administrator=True)
async def give(ctx, cost:int):
    with open('economy.json','r') as f:
        money = json.load(f)    
    emb = discord.Embed(description=f'**{ctx.author}** Вы выдали себе {cost} карбованців.')
    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    money[str(ctx.author.id)]['Money'] += cost
    with open('economy.json', 'w') as f:
        json.dump(money,f)
    await ctx.send (embed= emb)


#$timely - бонус 1000 карбованцівок передать.
@Bot.command()
async def bonus(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)    
        money_bonus = randint (1000, 20000)
    if not str(ctx.author.id) in bonus1:
        emb = discord.Embed(description=f'**{ctx.author}** Вы получили бонус в качетсве {money_bonus} карбованців.')
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send (embed= emb)
        money[str(ctx.author.id)]['Money'] += money_bonus
        bonus1.append(str(ctx.author.id))
        with open('economy.json', 'w') as f:
            json.dump(money,f)
        await asyncio.sleep(12*60*60)
        bonus1.remove(str(ctx.author.id))
    if str(ctx.author.id) in bonus1:
        emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили бонус.')
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send (embed= emb)

#$timely - бонус 1000 карбованцівок передать.
@Bot.command()
async def timely(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)    
    if not str(ctx.author.id) in money:
        money[str(ctx.author.id)] = {}
        money[str(ctx.author.id)]['Money'] = 0
    money_timely = 4000
    if not str(ctx.author.id) in queue:
        emb = discord.Embed(description=f'**{ctx.author}** Вы получили свои {money_timely} карбованців.')
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send (embed= emb)
        money[str(ctx.author.id)]['Money'] += money_timely
        queue.append(str(ctx.author.id))
        with open('economy.json', 'w') as f:
            json.dump(money,f)
        await asyncio.sleep(10*60)
        queue.remove(str(ctx.author.id))
    if str(ctx.author.id) in queue:
        emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свои {money_timely} карбованців.')
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send (embed= emb)

#$casino - бонус 1000 карбованцівок передать.
@Bot.command()
async def casino(ctx, cost:int):
    with open('economy.json','r') as f:
        money = json.load(f)    
    if money[str(ctx.author.id)]['Money'] < cost:
        emb = discord.Embed(description=f'**{ctx.author}** Недостаточно средств.')
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send (embed= emb)
    if money[str(ctx.author.id)]['Money'] >= cost:
        money[str(ctx.author.id)]['Money'] -= cost
        random_casino = randint(0, 12)
        if random_casino <= 2:
            random_casino = 0
        if random_casino == 3 <= 9:
            random_casino = 2
        if random_casino > 10:
            random_casino = 4
        if random_casino == 2:
            moneyx2 = int(random_casino*cost)
            money[str(ctx.author.id)]['Money'] += moneyx2
            emb = discord.Embed(description=f'**{ctx.author}** Вам выпал 2X. Вы выиграли {moneyx2} карбованців.')
            await ctx.send (embed= emb)
        if random_casino == 0:
            moneyx0 = random_casino*cost
            money[str(ctx.author.id)]['Money'] += moneyx0
            emb = discord.Embed(description=f'**{ctx.author}** Вам выпал 0X. Вы проиграли, ваша сумма пошла в казино.')
            await ctx.send (embed= emb)
        if random_casino == 4:
            moneyx4 = random_casino*cost
            money[str(ctx.author.id)]['Money'] += moneyx4
            emb = discord.Embed(description=f'**{ctx.author}** Вам выпал 4X. Вы выиграли {moneyx4} карбованців.')
            await ctx.send (embed= emb)
    with open('economy.json', 'w') as f:
        json.dump(money,f)

value_s = ['🍆',  '🍇', '🍌', '🍏', '🍒']

#$casino - бонус 1000 карбованцівок передать.
@Bot.command()
async def roulette(ctx, cost:int):
    with open('economy.json','r') as f:
        money = json.load(f)    
    if money[str(ctx.author.id)]['Money'] < cost:
        emb = discord.Embed(description=f'**{ctx.author}** Недостаточно средств.')
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send (embed= emb)
    if money[str(ctx.author.id)]['Money'] >= cost:
        money[str(ctx.author.id)]['Money'] -= cost
        value1 = randint(0, 4)
        value2 = randint(0, 4)
        value3 = randint(0, 4)
        value4 = value_s[value1]
        value5 = value_s[value2]
        value6 = value_s[value3]
        emb1 = discord.Embed(title='Рулетка', description='Рулетка, выберает 3 любых числа. Правила: Если выпадет три одинаковых числа - х4, если два - 2х, если ноль соответствий = 0х.', color= discord.Color.green())
        emb1.add_field(name="Значение 1:", value=value4)
        emb1.add_field(name="Значение 2:", value='☐')
        emb1.add_field(name="Значение 3:", value='☐')
        emb1.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        emb2 = Embed(title='Рулетка', description='Рулетка, выберает 3 любых числа. Правила: Если выпадет три одинаковых числа - х4, если два - 2х, если ноль соответствий = 0х.', color= discord.Color.green())
        emb2.add_field(name="Значение 1:", value=value4)
        emb2.add_field(name="Значение 2:", value=value5)
        emb2.add_field(name="Значение 3:", value='☐')
        emb2.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        emb3 = Embed(title='Рулетка', description='Рулетка, выберает 3 любых числа. Правила: Если выпадет три одинаковых числа - х4, если два - 2х, если ноль соответствий = 0х.', color= discord.Color.green())
        emb3.add_field(name="Значение 1:", value=value4)
        emb3.add_field(name="Значение 2:", value=value5)
        emb3.add_field(name="Значение 3:", value=value6)
        emb3.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        msg = await ctx.send(embed= emb1)
        await asyncio.sleep(1)
        await msg.edit(embed= emb2)
        await asyncio.sleep(1)
        await msg.edit(embed= emb3)
        if value1 == value2 == value3:
            money123x4 = int(cost*4)
            money[str(ctx.author.id)]['Money'] += money123x4
            emb4 = discord.Embed(description=f'Вам выпали 3 одинаковых числа. Вы получаете в 4 раза больше. Вы выиграли {money123x4} карбованців.', color= discord.Color.green())
            emb4.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed= emb4)
        else:
            if value1 == value2 or value1 == value3 or value3 == value2 or value2 == value3 or value2 == value1 or value3 == value1:
                money123x2 = int(cost*2)
                money[str(ctx.author.id)]['Money'] += money123x2
                emb5 = discord.Embed(description=f'Вам выпали 2 одинаковых числа. Вы получаете в 2 раза больше. Вы выиграли {money123x2} карбованців.', color= discord.Color.green())
                emb5.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed= emb5)
            else:
                emb6 = discord.Embed(description=f'Вам не выпали одинаковые числа. Вы проиграли {cost} карбованців.', color= discord.Color.green())
                emb6.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed= emb6)
    with open('economy.json', 'w') as f:
        json.dump(money,f)

#$balance - для проверки баланса.
@Bot.command()
async def balance(ctx, member:discord.Member = None):
    if member == ctx.author or member == None:
        with open('economy.json','r') as f:
            money = json.load(f)
        emb = discord.Embed(description=f'Ваш баланс: {money[str(ctx.author.id)]["Money"]} карбованців')
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed= emb)
    else:
        with open('economy.json','r') as f:
            money = json.load(f)
            emb = discord.Embed(description=f'Баланс **{member}**: {money[str(member.id)]["Money"]} карбованців')
            emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed= emb)
        
#$addrole - добавить роль в магазин.
@Bot.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, role:discord.Role,cost:int):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(role.id) in money['shop']:
        await ctx.send(f"Роль {role.mention} уже есть в магазине")
    if not str(role.id) in money['shop']:
        money['shop'][str(role.id)] ={}
        money['shop'][str(role.id)]['Cost'] = cost
        await ctx.send(f'Роль {role.mention} добавлена в магазин')
    with open('economy.json', 'w') as f:
            json.dump(money,f)

#$shop - список доступных товаров в магазине.
@Bot.command()
async def shop(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    emb = discord.Embed(title="Магазин",description = 'Здесь вы можете приобрести себе роль, или любой предмет, который выставлен сюда.')
    for role in money['shop']:
        emb.add_field(name=f'Цена: {money["shop"][role]["Cost"]}', value=f'<@&{role}>', inline= False)
    await ctx.send(embed = emb)

#$delrole - добавить роль в магазин.
@Bot.command()
@commands.has_permissions(administrator=True)
async def delrole(ctx, role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str(role.id) in money['shop']:
        await ctx.send("Роль отсутствует в магазине.")
    if str(role.id) in money['shop']:
        await ctx.send(f'Роль <@&{role.id}> удалена из магазина.')
        del money['shop'][str(role.id)]
    with open('economy.json', 'w') as f:
        json.dump(money,f)


#$buy - покупка роли из магазина.
@Bot.command()
async def buy(ctx, role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(role.id) in money['shop']:
        if money['shop'][str(role.id)]['Cost'] <= money[str(ctx.author.id)]['Money']:
            if not role in ctx.author.roles:
                await ctx.send(f'Вы купили роль <@&{role.id}>')
                for i in money['shop']:
                    if i == str(role.id):
                        buy = discord.utils.get(ctx.guild.roles,id = int(i))
                        await ctx.author.add_roles(buy)
                        money[str(ctx.author.id)]['Money'] -= money['shop'][str(role.id)]['Cost']
            else:
                await ctx.send(f'У вас уже есть роль <@&{role.id}>')
    with open('economy.json', 'w') as f:
        json.dump(money,f)



#<==================================================================>
#<==================================================================>
    

@Bot.command()
async def info(ctx, member:discord.Member):
    emb = discord.Embed(title='Информация о пользователе',description='Здесь будет отображаться информация о пользователе.',color=0x4298f5)
    emb.add_field(name="Имя пользователя:", value=member.display_name, inline=False)
    emb.add_field(name="Идентификатор пользователя:", value=member.id, inline=False)
    emb.add_field(name="Когда присоеденился на сервер:", value=member.joined_at, inline=False)
    emb.add_field(name="Аккаунт был создан:", value=member.created_at.strftime("%a, %#a %B %Y, %I:%M %p UTC"), inline=False)
    emb.set_thumbnail(url=member.avatar_url)
    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed = emb)

@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def all(ctx, *, reason):
    emb3 = discord.Embed(title="ALL", description='Вы были вызваны администратором.', color=0xff0000)
    emb3.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb3.add_field(name='Причина вызова:', value=reason, inline=False)
    emb3.add_field(name='Присоеденитесь в любой голосовой канал.', value=f'@everyone', inline=False)
    await ctx.send(embed = emb3)

@Bot.command()
async def who(ctx, *, who):
    a = ['Я думаю, что', 'Возможно, это', 'Может быть, это', 'Мне кажется, что']
    b = randint(0, 3)
    c = a[b]
    d = ['@Dx.TrpS#1114', '@platina300#2529', '@Dx.TrpS#1114', '@Yakov#0015', '@shooter#3584', '@не буде діла#1706', '@Феликс Эдмунович Дзержинсикий#7133', '@Серёжка Фонталин#2989', '@Быдло#4821', '@Воровская звезда#3929', '@12 y.o#9409']
    j = randint(0, 10)
    random_user = d[j]
    await ctx.send(f'{c} {random_user} {who}')

@Bot.command()
async def pr(ctx, *, who):
    a = ['Я думаю, что', 'Возможно,', 'Может быть,', 'Мне кажется,']
    b = randint(0, 3)
    c = a[b]
    proc = randint(0, 100)
    await ctx.send(f'{c} {who} на {proc}%')



@Bot.command()
async def random(ctx, number:int, number1:int):
    emb3 = discord.Embed(title="Random", description='Бот случайным образом выбирает значение из двух заданных ему переменных.', color=0xff0000)
    emb3.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    random_number = randint(int(number), int(number1))
    emb3.add_field(name='Выпал:', value=random_number, inline=False)
    await ctx.send(embed = emb3)

@Bot.command()
async def invite(ctx, member:discord.Member):
    emb3 = discord.Embed(title="Invete", description='', color=0xff0000)
    emb3.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb3.add_field(name='Вас приглашают на прием к психатерапевту, пожалуйста, пройдите в любой голосовой канал.', value=member.mention, inline=False)
    await ctx.send(embed = emb3)

@Bot.command()
async def recept(ctx, member:discord.Member, namelek, desc):
    emb3 = discord.Embed(title="Recept", description='', color=0xff0000)
    emb3.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb3.set_thumbnail(url='https://i.imgur.com/drLhawu.png')
    emb3.add_field(name='Рецепт на имя', value=member.mention, inline=False)
    emb3.add_field(name='Рецерт был выписан', value=ctx.message.author.mention, inline=False)
    emb3.add_field(name='Название лекарства', value=namelek, inline=False)
    emb3.add_field(name='Дискрипция', value=desc, inline=False)
    await ctx.send(embed = emb3)

@Bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()

@Bot.command()
async def coin(ctx):
    emb2 = discord.Embed(title="Coin", description='Бот случайным образом выбирает два значения: «Орел, или решка»', color=0xff0000)
    emb2.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    random = randint(0, 1)
    if random > 0:
        emb2.add_field(name='Выпал:', value='Орёл', inline=False)
    else:
        emb2.add_field(name='Выпала:', value='Решка', inline=False)
    await ctx.send(embed = emb2)

@Bot.event
async def on_ready():
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'============================================================================================')
    print(f'Бот запущен, и полностью готов к работе. Удачного дня, Тимур.')
    print(f'============================================================================================')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    print(f'')
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за дотерами"))



Bot.run('Nzg5MDk0NjUxNzM0MzkyODcy.X9tDqQ.g4KR107yvAMBNfGWQoBOOYDUwms')
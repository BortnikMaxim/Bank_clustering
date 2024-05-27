import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext
import os

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# File paths
loan_files = {
    'loan_1_year': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_loan_1_year.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_loan_1_year.xlsx',
    },
    'loan_3_years': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_loan_3_years.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_loan_3_years.xlsx',
    },
    'loan_5_years': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_loan_5_years.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_loan_5_years.xlsx',
    },
    'loan_10_years': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_loan_10_years.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_loan_10_years.xlsx',
    }
}

deposit_files = {
    'deposit_1_month': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_deposit_1_month.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_deposit_1_month.xlsx',
        '2': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_2_deposit_3_month.xlsx'
    },
    'deposit_3_months': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_deposit_3_months.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_deposit_3_months.xlsx',
    },
    'deposit_6_months': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_deposit_6_months.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_deposit_6_months.xlsx',
    },
    'deposit_1_year': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_deposit_1_year.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_deposit_1_year.xlsx',
        '2': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_2_deposit_1_year.xlsx'
    },
    'deposit_3_years': {
        '0': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_0_deposit_3_years.xlsx',
        '1': '/Users/maximbortnik/Desktop/ALL/FINAL DATA/bot/cluster_1_deposit_3_years.xlsx',
    }
}

# Cluster descriptions
cluster_descriptions = {
    'deposit_1_month': [
        "Average change in minimum interest rates -0.031%, average change in maximum interest rates 0.007%",
        "Average change in minimum interest rates -1.71%, average change in maximum interest rates -1.71%",
    ],
    'deposit_3_months': [
        "Average change in minimum interest rates -0.029%, average change in maximum interest rates -0.016%",
        "Average change in minimum interest rates 1.725%, average change in maximum interest rates 1.339%",
        "Average change in minimum interest rates -2%, average change in maximum interest rates -2%"
    ],
    'deposit_6_months': [
        "Average change in minimum interest rates -0.013%, average change in maximum interest rates 0.011%",
        "Average change of minimum interest rates 2.88%, average change of maximum interest rates 1.32%",
    ],
    'deposit_1_year': [
        "Average change in minimum interest rates 1.838%, average change in maximum interest rates 1.18%",
        "Average change in minimum interest rates -0.039%, average change in maximum interest rates -0.035%",
    ],
    'deposit_3_years': [
        "Average change in minimum interest rates 2.5%, average change in maximum interest rates 2.4%",
        "Average change in minimum interest rates -0.011%, average change in maximum interest rates -0.034%",
    ],
    'loan_1_year': [
        "Average change in minimum interest rates -0.045%, average change in maximum interest rates -0.144%",
        "Average change in minimum interest rates -2%, average change in maximum interest rates 13.303%",
        "Average change in minimum interest rates 4.8%, average change in maximum interest rates 5.175%"
    ],
    'loan_3_years': [
        "Average change in minimum interest rates -0.179%, average change in maximum interest rates -0.036%",
        "Average change in minimum interest rates 4.238%, average change in maximum interest rates 4.546%"
    ],
    'loan_5_years': [
        "Average change in minimum interest rates -0.204%, average change in maximum interest rates 0.022%",
        "Average change in minimum interest rates 4.589%, average change in maximum interest rates 4.2%",
    ],
    'loan_10_years': [
        "Average change in minimum interest rates 0.133%, average change in maximum interest rates 0.232%",
        "Average change in minimum interest rates 2.167%, average change in maximum interest rates 12.803%",
    ]
}

# Function to start the bot and display initial options
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_text(f'Hello, {user.first_name}. This bot demonstrates the clustering of Russian banks.')
    keyboard = [
        [InlineKeyboardButton('Deposits', callback_data='deposit')],
        [InlineKeyboardButton('Loans', callback_data='loan')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('To continue, please choose:', reply_markup=reply_markup)

# Function to handle button clicks
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    logger.info(f"Button pressed with callback data: {query.data}")

    if query.data == 'deposit':
        terms_keyboard = [
            [InlineKeyboardButton('1 month', callback_data='deposit_1_month')],
            [InlineKeyboardButton('3 months', callback_data='deposit_3_months')],
            [InlineKeyboardButton('6 months', callback_data='deposit_6_months')],
            [InlineKeyboardButton('1 year', callback_data='deposit_1_year')],
            [InlineKeyboardButton('3 years', callback_data='deposit_3_years')],
        ]
        reply_markup = InlineKeyboardMarkup(terms_keyboard)
        await query.edit_message_text('Choose the term for deposits:', reply_markup=reply_markup)
    
    elif query.data == 'loan':
        terms_keyboard = [
            [InlineKeyboardButton('1 year', callback_data='loan_1_year')],
            [InlineKeyboardButton('3 years', callback_data='loan_3_years')],
            [InlineKeyboardButton('5 years', callback_data='loan_5_years')],
            [InlineKeyboardButton('10 years', callback_data='loan_10_years')],
        ]
        reply_markup = InlineKeyboardMarkup(terms_keyboard)
        await query.edit_message_text('Choose the term for loans:', reply_markup=reply_markup)
    
    elif query.data.startswith('deposit_') or query.data.startswith('loan_'):
        term = query.data
        descriptions = cluster_descriptions.get(term, [])
        description_text = '\n'.join([f'Cluster {i}: {desc}' for i, desc in enumerate(descriptions)])
        await query.edit_message_text(f'You selected {term.replace("_", " ")}.\n\n{description_text}')
        
        clusters_keyboard = [
            [InlineKeyboardButton(f'Cluster {i}', callback_data=f'{term}_cluster_{i}')] for i in range(len(descriptions))
        ]
        reply_markup = InlineKeyboardMarkup(clusters_keyboard)
        await query.message.reply_text('See in details', reply_markup=reply_markup)
    
        # Conditions for sending deposit files
        if query.data == 'deposit_1_month_cluster_0':
            await query.edit_message_text("В этом кластере представлены: Абсолют Банк, Авангард, Агророс, Акибанк, Банк «Санкт-Петербург», Банк ВБРР, Банк ЗЕНИТ, Банк Казани, Банк РМП, Банк РСИ, Банк Синара (СКБ-банк), БыстроБанк, Газпромбанк, Газэнергобанк, Гарант-инвест, Генбанк, Держава, Джей энд ти Банк, Еврофинанс Моснарбанк, Живаго Банк, Зираат Банк Москва, ИК Банк, Инбанк, Ишбанк, Капитал, Клюква, Металлинвестбанк, Мир Бизнес Банк, Мир привилегий, Москва-Сити, Московский Кредитный Банк, Москомбанк, Москоммерцбанк, Муниципальный Камчатпрофитбанк, Национальный стандарт, Новый век, Ноосфера, Норвик Банк, ПСБ, Пересвет, Петербургский социальный коммерческий Банк, Примсоцбанк, ПроБанк, РБА, РОССИЯ, Развитие-столица, Росдорбанк, Россита-Банк, Россия, Сбербанк, Синко-Банк, Совкомбанк, Солид Банк, Тимер Банк, Тольяттихимбанк, Ури Банк, Финам, Фора-Банк, ЦМРБанк, Центрокредит, Экспобанк, Энерготрансбанк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_1_month']['0'], 'rb'))
        elif query.data == 'deposit_1_month_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Агора, Кредит Европа Банк (Россия), Нацинвестпромбанк, Прио-Внешторгбанк, СДМ-Банк.")            
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_1_month']['1'], 'rb'))
        elif query.data == 'deposit_3_months_cluster_0':
            await query.edit_message_text("В этом кластере представлены: Абсолют Банк, Авангард, Агропромкредит, Акибанк, Акцепт, Александровский, Альфа-Банк, ББР Банк, БКС Банк, Банк «Санкт-Петербург», Банк БЖФ, Банк ВБРР, Банк Глобус, Банк ДОМ.РФ, Банк ЗЕНИТ, Банк Интеза, Банк Казани, Банк Оранжевый, Банк РМП, Банк Раунд, Банк СГБ, Банк Синара (СКБ-банк), Банк Финсервис, БыстроБанк, ВТБ, Внешфинбанк, Газпромбанк, Газтрансбанк, Газэнергобанк, Гарант-инвест, Генбанк, Держава, Дружба, Евроальянс, Еврофинанс Моснарбанк, Живаго Банк, Зираат Банк Москва, ИК Банк, Инбанк, Инвестторгбанк, Ингосстрах Банк, Интерпрогрессбанк, Ишбанк, КБ Солидарность, Камкомбанк, Капитал, Клюква, Космос, Кошелев-Банк, Крокус-Банк, Кубань Кредит, Ланта-Банк, Локо-Банк, МБА-Москва, МТС-Банк, Международный финансовый клуб, Металлинвестбанк, Меткомбанк, Мир Бизнес Банк, Мир привилегий, Морской Банк, Москва-Сити, Московский Кредитный Банк, Москомбанк, Москоммерцбанк, Муниципальный Камчатпрофитбанк, НДБанк, НК Банк, НС Банк, Нацинвестпромбанк, Национальный резервный Банк, Национальный стандарт, Новикомбанк, Новый век, Ноосфера, Норвик Банк, ОЗОН Банк, ОТП Банк, ПСБ, Пересвет, Петербургский социальный коммерческий Банк, Почта Банк, Приморье, Примсоцбанк, ПроБанк, РБА, РЕСО Кредит, РЕСО кредит, РНКБ, РОСБАНК, РОССИЯ, Реалист Банк, Ренессанс Банк, Росдорбанк, Россита-Банк, Россия, Русский стандарт, Русьуниверсалбанк, СДМ-Банк, Сбербанк, Свой Банк, Синко-Банк, Славия, Совкомбанк, Солид Банк, Социум-Банк, Таврический, Тендер-Банк, Тимер Банк, Тольяттихимбанк, Транскапиталбанк, Трансстройбанк, Углеметбанк, Ури Банк, Финам, Финстар Банк, Фора-Банк, Хоум Банк, ЦМРБанк, Экспобанк, Энерготрансбанк, Эс-Би-Ай Банк, ЮниКредит Банк, Яндекс Банк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_3_months']['0'], 'rb'))
        elif query.data == 'deposit_3_months_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Агора, Азиатско-Тихоокеанский Банк, Ак Барс Банк, БКФ, Банк Синара (СКБ-банк), Банк Уралсиб, Кредит Европа Банк (Россия), Национальный Банк сбережений, Первый Инвестиционный Банк, Прио-Внешторгбанк, Россельхозбанк, Тинькофф Банк, Уральский Банк реконструкции и развития.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_3_months']['1'], 'rb'))
        elif query.data == 'deposit_3_months_cluster_2':
            await query.edit_message_text("В этом кластере представлены: БКС Банк")            
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_3_months']['2'], 'rb'))
        elif query.data == 'deposit_6_months_cluster_0':
            await query.edit_message_text("В этом кластере представлены: Абсолют Банк, Авангард, Автоторгбанк, Агропромкредит, Азиатско-Тихоокеанский Банк, Ак Барс Банк, Акибанк, Акцепт, Александровский, Алеф-Банк, Альфа-Банк, ББР Банк, БКС Банк, Банк «Санкт-Петербург», Банк БЖФ, Банк ВБРР, Банк Глобус, Банк ДОМ РФ, Банк ЗЕНИТ, Банк Интеза, Банк Казани, Банк Оранжевый, Банк РМП, Банк Раунд, Банк СГБ, Банк Уралсиб, БыстроБанк, ВТБ, Внешфинбанк, Газпромбанк, Газтрансбанк, Газэнергобанк, Гарант-инвест, Генбанк, Держава, Джей энд ти Банк, Евроальянс, Еврофинанс Моснарбанк, Живаго Банк, Зираат Банк Москва, Инбанк, Инвестторгбанк, Ингосстрах Банк, Интерпрогрессбанк, Ишбанк, КБ Солидарность, Камкомбанк, Капитал, Клюква, Космос, Кошелев-Банк, Крокус-Банк, Кубань Кредит, Локо-Банк, МБА-Москва, МТИ Банк, МТС-Банк, Международный финансовый клуб, Металлинвестбанк, Меткомбанк, Мир Бизнес Банк, Мир привилегий, Морской Банк, Москва-Сити, Московский Кредитный Банк, Москомбанк, Москоммерцбанк, Муниципальный Камчатпрофитбанк, НДБанк, НК Банк, НС Банк, Нацинвестпромбанк, Национальный Банк сбережений, Национальный резервный Банк, Национальный стандарт, Новикомбанк, Новый Московский Банк, Новый век, Ноосфера, Норвик Банк, ОЗОН Банк, ОТП Банк, ПСБ, Первый Инвестиционный Банк, Пересвет, Петербургский социальный коммерческий Банк, Почта Банк, Приморье, Примсоцбанк, Прио-Внешторгбанк, ПроБанк, Промтрансбанк, РБА, РЕСО Кредит, РОСБАНК, РОССИЯ, Реалист Банк, Ренессанс Банк, Росдорбанк, Россита-Банк, Ростфинанс, Русский стандарт, СДМ-Банк, Сбербанк, Свой Банк, Синко-Банк, Славия, Совкомбанк, Солид Банк, Социум-Банк, Таврический, Тендер-Банк, Тимер Банк, Тольяттихимбанк, Транскапиталбанк, Трансстройбанк, Углеметбанк, Уральский Банк реконструкции и развития, Финам, Финстар Банк, Фора-Банк, Хоум Банк, ЦМРБанк, Центрокредит, Цифра банк, Экспобанк,  Энерготрансбанк,  Эс-Би-Ай Банк,  ЮниКредит Банк,  Яндекс Банк")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_6_months']['0'], 'rb'))
        elif query.data == 'deposit_6_months_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Агора,  Банк Синара (СКБ-банк),  Кредит Европа Банк (Россия),  Россельхозбанк,  Тинькофф Банк")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_6_months']['1'], 'rb'))
        elif query.data == 'deposit_1_year_cluster_0':
            await query.edit_message_text("В этом кластере представлены: Агора, Азиатско-Тихоокеанский Банк, Банк «Санкт-Петербург», Банк Синара (СКБ-банк), Банк Уралсиб, Кредит Европа Банк (Россия), Меткомбанк, Нацинвестпромбанк, Прио-Внешторгбанк, Россельхозбанк, Тинькофф Банк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_1_year']['0'], 'rb'))
        elif query.data == 'deposit_1_year_cluster_1':
            await query.edit_message_text("Абсолют Банк, Авангард, Автоторгбанк, Агропромкредит, Ак Барс Банк, Александровский, Алеф-Банк, Альфа-Банк, ББР Банк, БКС Банк, БКФ, Банк БЖФ, Банк ВБРР, Банк Глобус, Банк ДОМ.РФ, Банк ЗЕНИТ, Банк Интеза, Банк Казани, Банк Оранжевый, Банк РМП, Банк Раунд, Банк СГБ, БыстроБанк, ВТБ, Внешфинбанк, Газпромбанк, Газтрансбанк, Газэнергобанк, Гарант-инвест, Генбанк, Держава, Джей энд ти Банк, Дружба, Евроальянс, Еврофинанс Моснарбанк, Живаго Банк, Зираат Банк Москва, Инбанк, Инвестторгбанк, Ингосстрах Банк, Интерпрогрессбанк, Ишбанк, КБ Солидарность, Капитал, Клюква, Космос, Кошелев-Банк, Кубань Кредит, Локо-Банк, МБА-Москва, МТИ Банк, МТС-Банк, Международный финансовый клуб, Металлинвестбанк, Мир Бизнес Банк, Мир привилегий, Морской Банк, Москва-Сити, Московский Кредитный Банк, Москомбанк, Москоммерцбанк, Муниципальный Камчатпрофитбанк, НДБанк, НК Банк, НС Банк, Национальный Банк сбережений, Национальный резервный Банк, Национальный стандарт, Новикомбанк, Новый Московский Банк, Ноосфера, Норвик Банк, ОЗОН Банк, ОТП Банк, ПСБ, Первый Инвестиционный Банк, Пересвет, Почта Банк, Приморье, Примсоцбанк, ПроБанк, Промтрансбанк, РБА, РЕСО Кредит, РЕСО кредит, РНКБ, РОСБАНК, РОССИЯ, Реалист Банк, Ренессанс Банк, Росдорбанк, Россита-Банк, Россия, Ростфинанс, Руснарбанк, Русский стандарт, СДМ-Банк, Сбербанк, Свой Банк, Синко-Банк, Славия, Совкомбанк, Солид Банк, Социум-Банк, Таврический, Тендер-Банк, Тимер Банк, Тольяттихимбанк, Транскапиталбанк, Трансстройбанк, Уральский Банк реконструкции и развития, Финам, Финстар Банк, Фора-Банк, Хоум Банк, ЦМРБанк, Центр-инвест, Центрокредит, Цифра банк, Экспобанк, Энерготрансбанк, Эс-Би-Ай Банк, ЮниКредит Банк, Яндекс Банк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_1_year']['1'], 'rb'))
        elif query.data == 'deposit_3_years_cluster_0':
            await query.edit_message_text("В этом кластере представлены: Кредит Европа Банк (Россия)")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_3_years']['0'], 'rb'))
        elif query.data == 'deposit_3_years_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Абсолют Банк, Агропромкредит, Азиатско-Тихоокеанский Банк, Ак Барс Банк, Альфа-Банк, ББР Банк, Банк «Санкт-Петербург», Банк ВБРР, Банк ДОМ.РФ, Банк ЗЕНИТ, Банк СГБ, Банк Синара (СКБ-банк), Банк Уралсиб, ВТБ, Газпромбанк, Газэнергобанк, Генбанк, Далена, Дружба, Евроальянс, Зираат Банк Москва, Инбанк, Инвестторгбанк, Ингосстрах Банк, Ишбанк, Металлинвестбанк, Московский Кредитный Банк, Муниципальный Камчатпрофитбанк, НОКССБАНК, НС Банк, Нацинвестпромбанк, Национальный резервный Банк, Новикомбанк, Норвик Банк, ПСБ, Почта Банк, Примсоцбанк, ПроБанк, РЕСО Кредит, РЕСО кредит, РНКБ, РОСБАНК, РОССИЯ, Реалист Банк, Ренессанс Банк, Россельхозбанк, Россия, Ростфинанс, Русский стандарт, СДМ-Банк, Сбербанк, Свой Банк, Совкомбанк, Солид Банк, Таврический, Транскапиталбанк, Трансстройбанк, Уральский Банк реконструкции и развития, Фора-Банк, Хоум Банк, Цифра банк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(deposit_files['deposit_3_years']['1'], 'rb'))

    # Conditions for sending loan files
        elif query.data == 'loan_1_year_cluster_0':
            await query.edit_message_text("В этом кластере представлены: Автоградбанк, Автокредитбанк, Агропромкредит, Азиатско-Тихоокеанский Банк, Ак Барс Банк, Акибанк, Акцепт, Алмазэргиэнбанк, Аресбанк, ББР Банк, Байкалкредобанк, Банк «Санкт-Петербург», Банк «Торжок», Банк Казани, Банк Оренбург, Банк РМП, Банк СГБ, Банк Синара (СКБ-банк), Банк Уралсиб, Банк Финсервис, Банк Хлынов, Банк ЧБРР, Белгородсоцбанк, Бизнес-Сервис-Траст, Братский АНКБ, Великие Луки банк, Вологжанин, Гарант-инвест, Генбанк, Дальневосточный Банк, Датабанк, Долинск, Дружба, Евроальянс, Енисейский объединенный Банк, Земский Банк, ИТ Банк, Ингосстрах Банк, Интерпрогрессбанк, Итуруп, Йошкар-Ола, КБ Солидарность, Калуга, Камкомбанк, Клюква, Континенталь, Кремлевский, Крокус-Банк, Крона-Банк, Кубаньторгбанк, Кузбассхимбанк, Кузнецкий, Курган, Ланта-Банк, Левобережный, Локо-Банк, МТС-Банк, Меткомбанк, Московский Кредитный Банк, Мурманский социальный коммерческий Банк, НБД-Банк, НИБ, НК Банк, Нальчик, Нацинвестпромбанк, Национальная Фабрика Ипотеки, Национальный Банк сбережений, Национальный стандарт, Нико-Банк, Новикомбанк, Новобанк, Новый век, Норвик Банк, ОТП Банк, ПСБ, Первоуральскбанк, Почтобанк, Приморье, Примсоцбанк, Приобье, Развитие-столица, Реалист Банк, Ренессанс Банк, Россельхозбанк, Ростфинанс, Русский стандарт, Русьуниверсалбанк, Сбербанк, СеверСтройБанк, Сервис резерв, Сити Инвест Банк, Совкомбанк, Солид Банк, Стройлесбанк, Сургутнефтегазбанк, Таганрогбанк, Тамбовкредитпромбанк, Татсоцбанк, Тинькофф Банк, Тольяттихимбанк, Томскпромстройбанк, Углеметбанк, Уралпромбанк, Уралфинанс, Уральский Банк реконструкции и развития, ФК Открытие, Фора-Банк, Центр-инвест, Центрокредит, Челиндбанк, Челябинвестбанк, Элита, Энерготрансбанк, Юг-Инвестбанк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_1_year']['0'], 'rb'))
        elif query.data == 'loan_1_year_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Альфа-Банк,  Саммит Банк,  Хоум Банк")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_1_year']['1'], 'rb'))
        elif query.data == 'loan_1_year_cluster_2':
            await query.edit_message_text("В этом кластере представлены: ВТБ,  Держава,  Живаго Банк,  Заречье,  Костромаселькомбанк,  Кузнецкбизнесбанк,  Сибсоцбанк,  Экспобанк")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_1_year']['0'], 'rb'))
        elif query.data == 'loan_3_years_cluster_0':
            await query.edit_message_text("В этом кластере представлены: Абсолют Банк, Автоградбанк, Автокредитбанк, Агропромкредит, Ак Барс Банк, Акибанк, Акцепт, Алеф-Банк, Алмазэргиэнбанк, Альфа-Банк, Аресбанк, ББР Банк, Байкалкредобанк, Банк «Санкт-Петербург», Банк «Торжок», Банк ВБРР, Банк ДОМ.РФ, Банк ЗЕНИТ, Банк Казани, Банк Оренбург, Банк РМП, Банк Раунд, Банк СГБ, Банк Синара (СКБ-банк), Банк Финсервис, Банк Хлынов, Банк ЧБРР, Белгородсоцбанк, Бизнес-Сервис-Траст, Братский АНКБ, Великие Луки банк, Венец, Владбизнесбанк, Вологжанин, Газпромбанк, Генбанк, Дальневосточный Банк, Датабанк, Долинск, Дружба, ЕАТПБанк, Евроальянс, Енисейский объединенный Банк, Земский Банк, ИК Банк, ИТ Банк, Инвестторгбанк, Ингосстрах Банк, Интерпрогрессбанк, Итуруп, Йошкар-Ола, КБ Солидарность, Калуга, Камкомбанк, Клюква, Континенталь, Кредит Урал Банк, Кремлевский, Крона-Банк, Кубань Кредит, Кубаньторгбанк, Кузбассхимбанк, Кузнецкбизнесбанк, Кузнецкий, Курган, Ланта-Банк, Локо-Банк, Левобережный, МТС-Банк, Меткомбанк, Московский Кредитный Банк, Муниципальный Камчатпрофитбанк, Мурманский социальный коммерческий Банк, НБД-Банк, НИБ, Нальчик, Нацинвестпромбанк, Национальная Фабрика Ипотеки, Национальный Банк сбережений, Национальный стандарт, Нико-Банк, Новикомбанк, Новобанк, Новокиб, Новый век, Норвик Банк, ОТП Банк, ПСБ, Первоуральскбанк, Пойдём!, Почта Банк, Почтобанк, Приморье, Примсоцбанк, Приобье, Промтрансбанк, РНКБ, РОСБАНК, РОССИЯ, Развитие-столица, Райффайзенбанк, Реалист Банк, Ренессанс Банк, Россельхозбанк, Россия, Ростфинанс, Русский стандарт, Сбербанк, СеверСтройБанк, Сервис резерв, Сибсоцбанк, Совкомбанк, Солид Банк, Ставропольпромстройбанк, Стройлесбанк, Сургутнефтегазбанк, Таганрогбанк, Тамбовкредитпромбанк, Татсоцбанк, Тинькофф Банк, Тольяттихимбанк, Томскпромстройбанк, Транскапиталбанк, Углеметбанк, Уралпромбанк, Уралфинанс, Уральский Банк реконструкции и развития, ФК Открытие, Фора-Банк, Форштадт, Центр-инвест, Центрокредит, Челиндбанк, Челябинвестбанк, Элита, Энергобанк, Энерготрансбанк, Юг-Инвестбанк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_3_years']['0'], 'rb'))
        elif query.data == 'loan_3_years_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Азиатско-Тихоокеанский Банк, ВТБ, Держава, Живаго Банк, Заречье, Костромаселькомбанк, Металлинвестбанк, Саммит Банк, Хакасский муниципальный банк, Хоум Банк, Экспобанк, ЮниКредит Банк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_3_years']['1'], 'rb'))
        elif query.data == 'loan_5_years_cluster_0':
            await query.edit_message_text("Абсолют Банк, Автоградбанк, Автокредитбанк, Агропромкредит, Ак Барс Банк, Акибанк, Алеф-Банк, Алмазэргиэнбанк, Альфа-Банк, Аресбанк, ББР Банк, Байкалкредобанк, Банк «Санкт-Петербург», Банк «Торжок», Банк БЖФ, Банк ВБРР, Банк ДОМ.РФ, Банк ЗЕНИТ, Банк Казани, Банк Оренбург, Банк РМП, Банк Раунд, Банк СГБ, Банк Синара (СКБ-банк), Банк Уралсиб, Банк Финсервис, Банк Хлынов, Банк ЧБРР, Белгородсоцбанк, Бизнес-Сервис-Траст, Братский АНКБ, Великие Луки банк, Венец, Владбизнесбанк, Вологжанин, Газпромбанк, Генбанк, Дальневосточный Банк, Датабанк, Долинск, Дружба, Евроальянс, Енисейский объединенный Банк, Земский Банк, ИТ Банк, Инвестторгбанк, Ингосстрах Банк, Интерпрогрессбанк, Итуруп, Йошкар-Ола, КБ Солидарность, Калуга, Камкомбанк, Клюква, Континенталь, Контур.Банк, Кредит Урал Банк, Кремлевский, Крона-Банк, Кубань Кредит, Кубаньторгбанк, Кузбассхимбанк, Кузнецкбизнесбанк, Кузнецкий, Курган, Ланта-Банк, Локо-Банк, МТС-Банк, Металлинвестбанк, Меткомбанк, Московский Кредитный Банк, Муниципальный Камчатпрофитбанк, Мурманский социальный коммерческий Банк, НБД-Банк, НИБ, НК Банк, Нальчик, Нацинвестпромбанк, Национальная Фабрика Ипотеки, Национальный стандарт, Нико-Банк, Новикомбанк, Новобанк, Новокиб, Новый век, Норвик Банк, ОТП Банк, ПСБ, Первоуральскбанк, Почта Банк, Почтобанк, Примсоцбанк, Приобье, Промтрансбанк, РОСБАНК, РОССИЯ, Развитие-столица, Райффайзенбанк, Реалист Банк, Ренессанс Банк, Россельхозбанк, Ростфинанс, Русский стандарт, Русьуниверсалбанк, Сбербанк, Свой Банк, СеверСтройБанк, Сибсоцбанк, Сити Инвест Банк, Совкомбанк, Солид Банк, Ставропольпромстройбанк, Стройлесбанк, Сургутнефтегазбанк, Таганрогбанк, Тамбовкредитпромбанк, Татсоцбанк, Тинькофф Банк, Томскпромстройбанк, Транскапиталбанк, Углеметбанк, Уралпромбанк, Уралфинанс, Уральский Банк реконструкции и развития, ФК Открытие, Фора-Банк, Хакасский муниципальный банк, Хоум Банк, Центр-инвест, Центрокредит, Челиндбанк, Челябинвестбанк, Элита, Энергобанк, Энерготрансбанк, Юг-Инвестбанк, ")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_5_years']['0'], 'rb'))
        elif query.data == 'loan_5_years_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Азиатско-Тихоокеанский Банк, ВТБ,  Держава,  Живаго Банк,  Костромаселькомбанк,  Приморье,  Саммит Банк,  Экспобанк,  ЮниКредит Банк")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_5_years']['1'], 'rb'))
        elif query.data == 'loan_10_years_cluster_0':
            await query.edit_message_text("В этом кластере представлены : Абсолют Банк, Автокредитбанк, Ак Барс Банк, Акцепт, Альфа-Банк, Аресбанк, ББР Банк, Байкалкредобанк, Банк БЖФ, Банк ЗЕНИТ, Банк Оренбург, Банк СГБ, Банк Уралсиб, Белгородсоцбанк, ВТБ, Великие Луки банк, Газпромбанк, Генбанк, Дальневосточный Банк, Датабанк, Итуруп, КБ Солидарность, Камкомбанк, Клюква, Кредит Урал Банк, Кубань Кредит, Кузбассхимбанк, МТС-Банк, Московский Кредитный Банк, Нацинвестпромбанк, Национальная Фабрика Ипотеки, Нико-Банк, Новокиб, Первоуральскбанк, Промтрансбанк, Развитие-столица, Реалист Банк, Ростфинанс, Русский стандарт, Русьуниверсалбанк, Свой Банк, Совкомбанк, Стройлесбанк, Татсоцбанк, Тинькофф Банк, Томскпромстройбанк, Уральский Банк реконструкции и развития, Фора-Банк, Хакасский муниципальный банк, Экспобанк, Элита, Энерготрансбанк, Юг-Инвестбанк.")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_10_years']['0'], 'rb'))
        elif query.data == 'loan_10_years_cluster_1':
            await query.edit_message_text("В этом кластере представлены: Альфа-Банк,  Держава, Локо-Банк")
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(loan_files['loan_10_years']['1'], 'rb'))

if __name__ == '__main__':
    application = ApplicationBuilder().token('6377770270:AAGtUtKPR8l_343CJo1_YoiYxPBIgCIUUHI').build()

    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)

    application.add_handler(start_handler)
    application.add_handler(button_handler)

    application.run_polling()

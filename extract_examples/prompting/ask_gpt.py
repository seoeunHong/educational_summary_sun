import fitz
import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
# print("OPENAI API KEY: ", openai.api_key)
openai_model = "text-davinci-003"
'''
examples = [
    "People need vitamin D to help their bones get enough calcium so that the bones can be strong. People can get vitamin D from milk, fish, and mushrooms. People’s bodies can also make vitamin D when their skin absorbs light from the Sun. Which situation will most likely cause a person’s bones to become weak?\nA. The person spends a lot of time outside. \nB. The person avoids foods with vitamin D. \nC. The person eats cereal with milk for breakfast each morning. \nD. The person eats lots of fish that provide vitamin D.",
    "Black carp are fish that were brought to the United States in the 1970s. Some black carp escaped into rivers during floods. They began to eat mussels and snails. The way mussels and snails feed helps clean the water in a river. Which effects will most likely be caused by introducing black carp into new ecosystems? Select the two correct answers.\nA. Other types of fish will find new food sources. \nB. Some types of snails will disappear from the ecosystems. \nC. The water in rivers will become dirty as black carp eat more mussels. \nD. Plants that live in rivers will be healthier because fewer nutrients will be in the water. \nE. The number of large predators will increase because they will have more kinds of fish to eat.",
    "A scientist studied layers of rock on the side of a cliff. In the top layer of rock, she found fossilized sand dunes. In the middle layer of rock, she found fossils of coral, clamshells, and shark teeth. In the bottom layer of rock, she found fossils of fern leaves. What is the correct order of the environments of the three layers, from oldest to youngest? \nA. desert, ocean, forest \nB. desert, forest, ocean \nC. ocean, forest, desert \nD. forest, ocean, desert",
    "The wetlands of Louisiana are home to many plants and animals. Due to a rise in ocean levels, these wetlands are being covered by salt water. In order to save the wildlife, a community decides to build a canal. A canal carries water from a nearby river to the wetlands. Which evidence best supports the claim that a canal will help the plants and animals in the wetlands? \nA. A canal will carry sediment and nutrients into the wetlands. \nB. A canal will provide a path for water to wash away non-native fish. \nC. A canal will increase the level of ocean water so more fish can live there. \nD. A canal will allow new predators to move into the wetlands from river habitats.",
    "In the early 1900s, farmers plowed large areas of land to plant crops. This removed the natural grasses and trees. These plants had deep roots that kept the soil in place. In the 1930s, there was a long drought, so crops would not grow. This exposed large areas of bare soil. The wind picked up a large amount of soil and blew it away. After the drought ended, the U.S. government encouraged farmers to change their farming practices to prevent this from happening again. Which practice would best help the soil stay in place? \nA. planting only natural grasses and corn in the fields \nB. planting soybeans and corn in fields next to fields with cattle \nC. planting trees and grasses in areas between fields with crops \nD. building pipelines to carry large amounts of water to use in sprinklers in the fields",
]
'''


# extract text from pdf
def pdf_extract(file):
    doc = fitz.open(file)
    pages = []
    for page in doc:
        page_text = page.get_text()
        pages.append(page_text)
    return pages


def prompt_gpt(page):
    prompt = (
        "You are given text. "
        "This text may be a question or description from an exam PDF. "
        'If the text appears to be a description or question containing any extra resources such as diagram, pictures, graphs, charts, tables, and so on, please respond with "Skip."\n\n'
        "If the text satisfies the following conditions: \n"
        "1. It is not a description. \n"
        '2. It is a "word problem" that can be solved with the given passage alone. \n'
        "3. It does not contain any extra resources in the question. \n\n"
        'Example of the type of "word problem" to extract: \n'
        '"People need vitamin D to help their bones get enough calcium so that the bones can be strong. People can get vitamin D from milk, fish, and mushrooms. People’s bodies can also make vitamin D when their skin absorbs light from the Sun. Which situation will most likely cause a person’s bones to become weak?\nA. The person spends a lot of time outside. \nB. The person avoids foods with vitamin D. \nC. The person eats cereal with milk for breakfast each morning. \nD. The person eats lots of fish that provide vitamin D."\n'
        '"A scientist studied layers of rock on the side of a cliff. In the top layer of rock, she found fossilized sand dunes. In the middle layer of rock, she found fossils of coral, clamshells, and shark teeth. In the bottom layer of rock, she found fossils of fern leaves. What is the correct order of the environments of the three layers, from oldest to youngest? \nA. desert, ocean, forest \nB. desert, forest, ocean \nC. ocean, forest, desert \nD. forest, ocean, desert"\n\n'
        'Examples of text to respond with "Skip": \n'
        '"Read the sample and mark the correct answer.\n Students looked online for weather data of their city. The table shows the data. \nWeather Data\nMonday Tuesday Wednesday Thursday Friday\nLow Temperature (°F) High Temperature (°F) Wind\nRain (inches)\n70 72 68\n90 88 88 light medium strong\n0 1 2\n81 81\n93 95 light light 0 1\nBased on the data, which day had both the lightest wind and highest temperature?\nA. Friday\nB. Thursday\nC. Tuesday\nD. Monday"\n'
        '"Dolphins are sometimes seen in groups. The groups are called pods. The picture shows a pod of dolphins.\nA student claims that living in pods is better for the dolphins than living alone.\nWhich two activities are easier for dolphins because they live in a pod?\nM. communicating with different species P. swimming in calm waters\nR. breathing above the surface\nS. hunting for prey\nT. finding a mate"\n\n'
        f'Here is the text: "{page}"\n\n'
        'Return the original text of the "word problem" if it meets all these conditions. Do not modify the text in any way, including words or syntax.'
    )

    response = openai.Completion.create(
        model=openai_model,
        prompt=prompt,
        max_tokens=100,
    )
    return response.choices[0].text


def pipeline():
    file = "datasets/Grade3_Science_PracticeTest.pdf"
    results = []
    pages = pdf_extract(file)
    for page in pages[:6]:
        gpt_answer = prompt_gpt(page)
        if "Skip" not in gpt_answer and "skip" not in gpt_answer:
            print(gpt_answer)
            results.append(gpt_answer)
    json.dump(results, open(f"prompt_{openai_model}.json", "w"), indent=4)


if __name__ == "__main__":
    pipeline()

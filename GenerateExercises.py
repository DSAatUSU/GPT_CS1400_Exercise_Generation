import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import openai
from slugify import slugify

pathPrefix = 'generatedExercises/'

if (len(sys.argv) <= 1):
    print("Pass an argument representing the directory where you would like to store the generated exercises")
    sys.exit(1)

if (os.path.exists(pathPrefix + sys.argv[1])):
    print("Directory Should not exist so that this script doesn't accidentally overwrite a directory")
    sys.exit(2)


load_dotenv()

client = OpenAI()

categoriesFile = open("CategoryIdeas/InputList.md")

categories = {}

currentCat = ''

for line in categoriesFile:
    if (line.startswith("### ")):
        currentCat = line[4:]
        categories[currentCat] = []
        continue

    if (line.startswith("- ")):
        categories[currentCat].append(line[2:])

os.makedirs(pathPrefix + sys.argv[1])
for category in categories:
    for subCategory in categories[category]:
        path = pathPrefix + sys.argv[1] + '/' + slugify(category) + '/' + slugify(subCategory)
        os.makedirs(path)
        chat_log = [{
            'role': 'system',
            'content': '''
                You are an expert computer science educator.
                You have a class of students who have never programmed before.
                They have asked you to write some of the Hackerrank and
                Leetcode style programming exercises for them that
                you are so good at writing.
            '''
        }, {
            'role': 'user',
            'content': '''
                Write a programming exercise that falls within the main
                category {category} and the subcategory {sub}. It should be
                easy to know if you got it correct, it can have starter code,
                and it can have unit tests.
            '''.format(category=category, sub=subCategory)
        }]
        response = client.chat.completions.create(model="gpt-4-1106-preview", messages=chat_log)
        print(response)
        answer = response.choices[0].message.content

        new_f = open(path + '/' + slugify(subCategory[:60]) + ".result.txt", "w")
        new_f.write(answer)

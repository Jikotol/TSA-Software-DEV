# :wave: LearnSigns
A website built for TSA's 2025-2026 software development competition. Made to remove barriers in learning ASL with a personalized and easy-to-use, website. Designed for people with hearing impairments, but also to spread awareness and increase accessibility.

## :pencil2: Description
LearnSigns is a website to help users, from beginner to advanced. 

## :white_check_mark: Functional Features
  - **Vocab List** with linked videos(in the future), terms, and handshapes
  - **User Accounts** in order to save flashcard sets
  - **User Flashcard Sets** with custom info and formats
  - **SQL Relational Databases** to accurately represent ASL

## :wrench: In Progress
  - **CSS**
  - **Error Checking Code**
  - **Detailed Documentation**

## :sparkles: Future Features
  - **Anki-Inspired Flashcard Spacing** to enhance learning
  - **Quiz Mode** to solidify terms in a fun, easy way
  - **Articles** expanding past vocab
  - **Personalized Recommendations** to lower the barrier of learning
  - **Progress Tracking** to motivate users to continue learning

# Instructions to Run
``` bash
# Clone the repository
git clone <repo-url>
cd LearnSigns

# Install dependencies
pip install -r requirements.txt

# Run the app 
python3 app.py

# Open in browser
http://127.0.0.1:5000
```

### Build Info
LearnSigns uses a csv from the American Sign Language Linguistic Research Project(ASLLRP), which is a research based asl project which contains and categorizes various signs including variants(e.g. fingerspelled, handshape variations, different handedness, etc). LearnSigns takes that info and converts it into study-ready flashcards by inserting them into a relational dataset. This makes learning asl more in depth, due to more detail in the signs and, therefore, enhanced learning.
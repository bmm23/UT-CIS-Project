# UT-CIS-Project
From scraped UT CIS db + UT gpa distributions, produce difficulty model for users + analytics


Final Functionality:

User arrives to site, greeted with template of course analytics (grade histogram, difficulty)
"Begin input"
User selects courses + professor
  if course or prof not found, generalize data
Returns variety of graphs + difficulty scale for semester


GPA modeling

User inputs previous courses + grade in those courses
Difficulty applied to each course from GPA distribution
From previous grades, future courseload GPA modelled using calculated difficulty
  Difficulty = (prof reported difficulty - mean dept difficulty) / n courses
  Something about grade dist thrown in model

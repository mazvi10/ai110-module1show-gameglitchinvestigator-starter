# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?a
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  1. Pressing enter does not work and I expected it to work as it is an instruction
  2. Entering a new guess needs two clicks, whilst I expected an automatic enter-and-feedback process
  3. The debugger info does not reset history when a new game is initiated
  4. When it initially runs, one attempt has already been used up, but is not a problem after prompting a new game though
  5. Seems the 'go lower' and 'go higher' hints are switched 
  6. Counting of attempts is delayed
  7. Normal and hard ranges should be switched
  8. The game difficulty and range text is not updated on the game interface when changed in settings


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Guess = 70 (secret is 80)|'Go higher' hint |'Go lower' hint | none|
|Enter key pressed |The guess is entered |Nothing happens | none|
|New game button pressed |All the variables reset | Only secret and attempts reset, not history| none|
|Difficultly setting switched|The range changes on the interface| The range stays as 1 and 100| none|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used Claude on this project as it was suggested by the course. I also used ChatGPT to brush up on my bash commands

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  One AI suggestion that was removing the unnecessary stringifying of the even attempts. I verified this by looking through the code and seeing how it provided erratic results that caused glitches in the game. The AI's ultimate suggestion was removing that branch and always using the integer, which I did.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  One AI suggestion was how giving how an invalid input cost an attempt, however, I do not see that as an error as the instructions are clear to the user thus entering strings would be a willful attempt that should count as an attempt, even if it was an invalid input. 



---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I generated a pytest and ran that. I then proceeded to run the game multiple times only focussing on its behavior regarding the problem area to see if the error was fixed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  I did a pytest test and manual test for the check_guess function in which I had 3 test cases that had the correct guess, a too high guess and a too low guess. This test showed him how solving that one big bug cleared some minor bugs I had noted without necessarily focusing on them. It also, of course, showed me that the code was functional in that specific method, thus any other errors I would run into would be something that outside of the check_guess logic

- Did AI help you design or understand any tests? How?

  AI did help me create the pytest tests by generating some examples to assert in the test_game_logic file. It added a pytest.mark.parametrize section that does multiple guesses after the tests I had already made targeting the three instances of correct, low or high.



---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  I would say that Streamlit is a way to create a python web page that reruns all the python code, from top to bottom, whenever a change is made. However, session states allow specific variables to keep their values or progress whenever a rerun is done, whilst all the other variables are reset.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Creating pytest scripts in order to make sure functions are functional individually
- What is one thing you would do differently next time you work with AI on a coding task?
  I think I will be more clear on what bug i want to focus on at a time because the AI tends to want to fix all the bugs of the code, which can be overwhelming to comb through
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  It has changed how I interact with AI in the sense that I can use to first understand code I am not sure about then use it to fix only the bugs I am focused on. It has also helped me start using to do all the tedious coding tasks like refactoring and creating test cases

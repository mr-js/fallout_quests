# fallout_quests
 Build your own offline reference from online Fallout Wiki Fandom in one click

 ## Usage
 1. Check and set the definitions for each target Wiki according to the markup ("settings\\\*.py").
 2. Select the wiki to be processed by the program: remove "!" before the required file names.
 2. Check and set global parameters ("settings\\global.toml").
 4. Run "fallout_quests.py" -- program started.
 5. You can see the current progress in the console and in "fallout_quests.log".
 6. The results of the program by stages will appear sequentially as follows: started => ./game_name,  downloaded => ./game_name/raw, parsed and builded => ./game_name/html, compiled => ./game_name/index.html

 The program will automatically download the wiki content, analyze and parse it, then extract the necessary data and compile the offline reference for you.

 ## Examples
 Results of the program (fragments of the offline reference book):

 ---

 ![fallout_quests_0](/images/fallout_quests_0.png)

 ---

 ![fallout_quests_1](/images/fallout_quests_1.png)

 ---

 ![fallout_quests_2](/images/fallout_quests_2.png)

 ---

 ![fallout_quests_3](/images/fallout_quests_3.png)

 ---

 ## Remarks
 > [!NOTE]
 > So this is a huge process on such data volumes, you can separately download the content, parse the data, and build the library. For example, first set the "step_download" option to True and the other options to False, run the program for all active target encyclopedias on Fandom (see templates in "\settings") -- now you have a dump of the necessary data, after which you can separately parse and build various offline libraries (just remember to set the "step_download" option to False after the previous step).

 > [!IMPORTANT]
 > By launching this program, you actually download the full version of the content from the Fandom resource. Check your local laws to determine if this is legal.

 > [!WARNING]
 > Downloading just one Fandom encyclopedia requires the consumption of a large amount of Internet traffic (on the order of tens to hundreds of gigabytes). Check that this is suitable for you at the current time before starting the program.

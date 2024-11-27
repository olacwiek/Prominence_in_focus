#This script cuts out excerpts of sounds with specific labels (here: cuts out phrases according to specific words that the phrase contains) and saves them
#to separate wav files. It can process several files from a directory. ZM (modified Lennes)

form Cuts out excerpts of sounds with specific labels
    comment Directory of TextGrid files
    text textgrids_dir C:\Users\cwiek\OneDrive\Projects\MultIS-Collaboration\Analysis\MultIS_data\
    #text textgrids_dir /Users/zmalisz/Documents/prominence_PL_2014/Aprocess/
    sentence textgrid_extension .TextGrid
    comment Directory of sound files
    text soundfiles_dir C:\Users\cwiek\OneDrive\Projects\MultIS-Collaboration\Analysis\MultIS_data\
    #text soundfiles_dir /Users/zmalisz/Documents/prominence_PL_2014/Aprocess/
    sentence soundfile_extension .wav
    comment Give the folder where to save the sound files:
    sentence Folder C:\Users\cwiek\OneDrive\Projects\MultIS-Collaboration\Analysis\audio_processed\
    #sentence Folder /Users/zmalisz/Documents/prominence_PL_2014/perceptual_2014/
    comment Give an optional prefix for all filenames:
    sentence Prefix _
    comment Give an optional suffix for all filenames (.wav will be added anyway):
    sentence Suffix 
    comment Nr of phrase tier 
    integer phrase_tier_number 1
    comment Nr of words tier
    integer word_tier_number 2
endform

textgrids_list = Create Strings as file list... textgrids 'textgrids_dir$'*'textgrid_extension$'
textgrids_list_id = selected("Strings", -1)
number_of_sound_files = Get number of strings
	for i to number_of_sound_files
	# Read a TextGrid
	textgrid_file$ = Get string... i
	Read from file... 'textgrids_dir$''textgrid_file$'
	filename$ = selected$("TextGrid", -1)
	textgrid_id = selected("TextGrid",-1)
	
	#Read a sound file
	Open long sound file... 'soundfiles_dir$''filename$''soundfile_extension$'
	sound_id = selected("LongSound", -1)
	
	#Iterate over the TextGrid
	select textgrid_id
	no_words = Get number of intervals... word_tier_number
		for word to no_words
		word_label$ = Get label of interval... word_tier_number word
			if index_regex (word_label$, "G04_")
			word_time = Get start point... word_tier_number word
			phrase = Get interval at time... phrase_tier_number word_time
			phrase_label$ = Get label of interval... phrase_tier_number phrase
			intervalstart = Get start point... phrase_tier_number phrase
			intervalend = Get end point... phrase_tier_number phrase
			select sound_id
			Extract part... intervalstart intervalend rectangular 1.0 no
			# The name of the sound file then consists of these elements:
			intervalfile$ =  "'filename$'" + "'prefix$'" + "'phrase_label$'" + ".wav"
			Write to WAV file... 'intervalfile$'
			Remove
			endif
			select textgrid_id
		endfor
 	# Remove objects
    	select textgrid_id
   	plus sound_id
	Remove
	# Select the TextGrid  list
    	select textgrids_list_id
	endfor
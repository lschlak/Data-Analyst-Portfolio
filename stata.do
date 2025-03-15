
****************************************************
// Luke Schlake
// Excel Cleaning and Keyword Filtering in Stata
// Dec 15 2024
****************************************************


//Set Filepaths 

//Set filepath for source files 	
global sourcepath ""

//Set your working path for temporary files
global workingpath ""

//Set your output directory
global output ""


//Define File Names
local files 

//Define variables in dta
local vars A B C D E F G H I J K L M N O P Q R S TU V W X Y Z AA AB AC AD AE AF AG AH AI AJ AK AL AM AN AO AP

//Loop Through and Create Files

local sourcefiles: dir "$sourcepath"files "*" //Local to store variable names

//Initiate counter
local i =0

//Match Files names to first six digits of filename
foreach x in `files' { 						//Loop through files
	foreach f in `sourcefiles'{ 			//Loop through filenames
		local first_six = substr("`f'",1,6)	//Save first six digits of filename
		if "`x'"=="`first_six'" {			//If filename equals first siz digits
			local i=`i'+1					//Update counter
			di "Match `i': `x' and `f'"		//Print if successful match
	 
			import excel "$sourcepath\\`f'", sheet("Sheet Name") firstrow clear //Import Excel file if match
				
			gen id= _n 						//Generate id
			gen present =.					//Generate present variable
			gen Project_Name = "`x'"		//Generate project name variable, replace with file name
			order Project_Name id present 	//Reorder variable
			
			foreach v in `vars' {			//Loop through each variable in the dta
			capture confirm str variable `v' //Confirm variable is string
			if _rc {  						//If variable is not string
				di "(`n',`v'):Numeric"		//Print id and variable name
				}
			else { 							//If variable is string, replace "present" variable
				di "(`n',`v') String"		//Print id and variable name
				replace present=1 if regex(`v',"Keyword #1") //Replace present=1 if keyword #1 present
				replace present=1 if regex(`v',"Keyword #2") //Replace present=1 if keyword #2 present
				replace present=1 if regex(`v',"Keyword #3") //Replace present=1 if keyword #3 present
				replace present=1 if regex(`v',"Keyword #4") //Replace present=1 if keyword #4 present
				replace present=1 if regex(`v',"Keyword #5") //Replace present=1 if keyword #5 present
				replace present=1 if regex(`v',"Keyword #6") //Replace present=1 if keyword #6 present
				} 
			}		
		}
		else {
		}
	}	
	keep if present==1 //Drop rows without the keyword
	findname, all(missing(@)) 
	drop `r(varlist)'
	save "$workingpath\\`x'_working", replace //Save adjusted dta 
	clear
	set maxvar 15000						   
}

//Appending all cleaned files together: 
cd "$workingpath" //Set working directory

local files: dir "$workingpath"files "*.dta" //Set local to store working directory files
di `files' //Display filenames

local filesToAppend ""
foreach file in `files' {
		local filesToAppend "`filesToAppend' `file'"	 //Loop through files and add to filename variable
  }

local first = 1
foreach f in `filesToAppend' {  //Loop through local with each filename
        if `first' {			//If file is the first file, use it as the base dta
            use "`f'", clear
            local first = 0
        }						//For all other dta files, append to first dta file
        else {
			di "`f'"
            append using "`f'"  //Note: no force option on append function
        }
    }

	
//Redefine variables as neccessary, then reshape to wide: 
reshape wide SQ, i(Project_Name) j(labels) 
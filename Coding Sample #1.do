
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//  Code for Effects of Ideoogical Identification Paper (Writing Sample #1 in IDA Application)
//	Luke Schlake (Sole Code Author)
//	Dec 2023
//  Summary: This code uses data from the Prosecution Project dataset. The data is cleaned and then
	modeled using cross-validated two-part models to handle excessive zeroes. The results 
	can be found in the paper: "Effects of Ideological Identification on Sentencing for Criminal 
	Cases Involving Political Violence in Federal Cases" by Luke Schlake & Ethan Doshi
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/



//%%%%%%%%%%%%%%%%%%%%%%%%%% DATA IMPORT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

set more off
use "data_filepath", clear

//%%%%%%%%%%%%%%%%%%%%%%%%%% DATA CLEANING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

//Drop empty columns
forvalues i = 1(1)105 {
        drop x`i'
  }

// Create Necessary Dummy Variables 
// All variables for used in regression models begin with CAPITAL LETTERS: 

//Date
	gen Date = date(date, "MDY")
	format Date %td
	
	foreach x in 1990 1995 2000 2005 2010 2015 2020 2025{
		count if Date < td(01/01/`x')
	}
	count if Date < td(01/01/2000) //Count if cases occurred in specific time ranges
	count if Date > td(01/01/1990)
	count if Date > td(01/01/2015) 
	
// Number Killed
	destring xkilled, replace
	gen Xkilled = xkilled

// Number Injured
	destring xinjured, replace
	gen Xinjured = xinjured

// People vs. Property
	egen People_or_Property = group(peoplevsproperty), label

// Co-offender
	gen Cooffender =0
	destring cooffender, replace
	replace Cooffender=1 if cooffender ==1
	
// Physical target
	gen Physical_target =.
	replace Physical_target = 1 if physicaltarget == "Educational institution" 
	replace Physical_target = 2 if physicaltarget == "Federal site: judicial" | physicaltarget == "Federal site: military" | physicaltarget == "Federal site: non-U.S. embassy or consulate" | physicaltarget == "Federal site: non-military non-judicial"
	replace Physical_target = 3 if physicaltarget == "Individual person(s)"
	replace Physical_target = 4 if physicaltarget == "Mass transportation: air" | physicaltarget == "Mass transportation: ground" | physicaltarget == "Mass transportation: infrastructure" | physicaltarget == "Mass transportation: water" 
	replace Physical_target = 5 if physicaltarget == "Medical institution"
	replace Physical_target = 6 if physicaltarget == "Multiple types"
	replace Physical_target = 7 if physicaltarget == "Municipal: local law enforcement"
	replace Physical_target = 8 if physicaltarget == "No direct target"
	replace Physical_target = 9 if physicaltarget == "Online"
	replace Physical_target = 10 if physicaltarget == "Private site: business/corporate property" | physicaltarget == "Private site: residential" 
	replace Physical_target = 11 if physicaltarget == "Public site: event" | physicaltarget == "Public: commercial space of recreation" | physicaltarget == "Public: non-commercial space"
	replace Physical_target = 12 if physicaltarget ==  "Religious institution"
	replace Physical_target = 13 if physicaltarget =="State site: judicial" | physicaltarget == "State site: non-military non-judicial"
	replace Physical_target = 14 if physicaltarget == "Unspecified/unknown/undeveloped"

// Completion of Crime
	egen Completion_of_Crime = group(completionofcrime), label
	
// Criminal Method
	levelsof criminalmethod
	egen Criminal_Method = group(criminalmethod), label
	
//Jurdisdiction
	gen Jurisdiction = jurisdiction
	
//Plea
	levelsof plea
	gen Plea = plea

// Hate crime
	gen Hate_Crime = hatecrime
	
// Previous Similar Method
	gen Prev_Similar = previoussimilarmethod
	destring Prev_Similar, replace
	
//Gender
	levelsof gender 
	tabulate gender
	count if gender != "Male" & gender != "Female"
	gen Gender = 0 
	replace Gender = 1 if gender == "Female"

//Race
	tabulate racialethnicgroup
	egen Race = group(racialethnicgroup), label

//Citizenship
	tabulate citizenshipstatus
	gen US_Citizen = 0
	replace US_Citizen = 1 if citizenshipstatus == "U.S. citizen"

//Ideaological Affiliation
	tabulate ideologicalaffiliation
	graph bar (count), over(ideologicalaffiliation)
	gen Ideology = .
	replace Ideology = 2 if ideologicalaffiliation == "Leftist: eco-animal focused" | ideologicalaffiliation == "Leftist: government-focused" | ideologicalaffiliation == "Leftist: identity-focused"
	replace Ideology = 2 if ideologicalaffiliation == "Nationalist-separatist"
	replace Ideology = 1 if ideologicalaffiliation == "Rightist: abortion-focused" | ideologicalaffiliation == "Rightist: government-focused" | ideologicalaffiliation == "Rightist: identity-focused" | ideologicalaffiliation == "Rightist: unspecified"
	replace Ideology = 4 if ideologicalaffiliation == "Salafi/Jihadist/Islamist"
	replace Ideology = 5 if ideologicalaffiliation == "Other" | ideologicalaffiliation == "Unclear"
	replace Ideology = 6 if ideologicalaffiliation == "No affiliation/not a factor"
	 
// Veteran Status
	tabulate veteranstatus
	gen Veteran_Status = 1
	replace Veteran_Status = 0 if veteranstatus == "Civilian" | veteranstatus =="Former/current member of non-U.S. military"
	
//Age 
	destring age, replace
	sum age
	replace age =35.52 if age ==. //Replaces the missing age values with the mean of age
	gen Age = age
	
//Life Sentences
	drop if lifesentence =="X"
	destring lifesentence, replace
	replace lifesentence =1 if lifesentence > 0
	gen Life_Sentences = lifesentence

//Length of Prison Sentence 
	gen Length_of_Sentence = floor(lengthofprisonsentencemonths /36)
	
	

//%%%%%%%%%%%%%%%%%%%%%%%%%% MODELING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

//Define Independent Variables
	global independent Xkilled Xinjured i.Completion_of_Crime i.Criminal_Method  Plea Gender i.Race US_Citizen i.Ideology Veteran_Status i.Physical_target Cooffender Hate_Crime Prev_Similar
	global LS_dependent Life_Sentences
	global PT_dependent Length_of_Sentence

//Drop the Individuals with Life Sentences 
	drop if Life_Sentences == 1

//Model the Remaining Data
	*Logit + Poisson
	twopm $PT_dependent $independent, firstpart(logit) secondpart(glm, family(poisson)) vce(robust)
	estimates store twopm_pois
	
	*Logit + NegBi 
	twopm $PT_dependent $independent, firstpart(logit) secondpart(glm, family(nbinomial)) vce(robust)
	estimates store twopm_nbin
	
	*Logit + Gamma
	twopm $PT_dependent $independent, firstpart(logit) secondpart(glm, family(gamma)) vce(robust)
	estimates store twopm_exp
	
	**Output TWOPM Results in Word
	outreg2 [twopm_pois twopm_nbin twopm_exp] using "output_filepath", see replace

	*Hurdle: 
		*Logit
			qui logit $PT_dependent $independent
			estimates store logit
		*Truncated Poisson
			qui tpoisson $PT_dependent $independent if Length_of_Sentence > 0
			estimates store pois
		*Results 
			suest logit pois 

//Cross-Validation to Assess Two-Part Models
	set seed 108
	gen id = runiform()
	egen split10 = cut(id), group(10)

	*Logit + Poisson
			gen Two_Part_Pos_MSE=.
			qui forvalues i=0/10 {
				twopm $PT_dependent $independent, firstpart(logit) secondpart(glm, family(poisson)) vce(robust) if split10 != `i'
				predict yhat if !e(sample)
				replace Two_Part_Pos_MSE=(Length_of_Sentence-yhat)^2 if !e(sample)
				drop yhat
				}
			di "MSE: Two-Part Model: "
			sum  Two_Part_Pos_MSE
		
	*Logit + NegBi
			gen Two_Part_NBREG_MSE=.
			qui forvalues i=0/10 {
				twopm $PT_dependent $independent, firstpart(logit) secondpart(glm, family(nbinomial)) vce(robust)
		if split10 != `i'
				predict yhat if !e(sample)
				replace Two_Part_NBREG_MSE=(Length_of_Sentence-yhat)^2 if !e(sample)
				drop yhat
				}
			di "MSE: Two-Part Model: " 
			sum Two_Part_NBREG_MSE
		
	*Logit + Gamma
			gen Two_Part_Gamma_MSE=.
			qui forvalues i=0/10 {
				twopm $PT_dependent $independent, firstpart(logit) secondpart(glm, family(nbinomial)) vce(robust)
		if split10 != `i'
				predict yhat if !e(sample)
				replace Two_Part_Gamma_MSE=(Length_of_Sentence-yhat)^2 if !e(sample)
				drop yhat
				}
			di "MSE: Two-Part Model: " 
			sum Two_Part_Gamma_MSE
	





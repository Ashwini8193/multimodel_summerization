# -*- coding: utf-8 -*-
# @Author: Jie Yang
# @Date:   2019-03-29 16:10:23
# @Last Modified by:   Jie Yang,     Contact: jieynlp@gmail.com
# @Last Modified time: 2019-04-12 09:56:12


## convert the text/attention list to latex code, which will further generates the text heatmap based on attention weights.
import os
import sys
import numpy as np

latex_special_token = ["!@#$%^&*()"]

def generate(text_list, attention_list, latex_file, color='red', rescale_value = False):
	assert(len(text_list) == len(attention_list))
	if rescale_value:
		attention_list = rescale(attention_list)
	word_num = len(text_list)
	text_list = clean_word(text_list)
	with open(latex_file,'w') as f:
		f.write(r'''\documentclass[varwidth]{standalone}
\special{papersize=210mm,297mm}
\usepackage{color}
\usepackage{tcolorbox}
\usepackage{CJK}
\usepackage{adjustbox}
\tcbset{width=0.9\textwidth,boxrule=0pt,colback=red,arc=0pt,auto outer arc,left=0pt,right=0pt,boxsep=5pt}
\begin{document}
\begin{CJK*}{UTF8}{gbsn}'''+'\n')
		string = r'''{\setlength{\fboxsep}{0pt}\colorbox{white!0}{\parbox{0.9\textwidth}{'''+"\n"
		for idx in range(word_num):
			string += "\\colorbox{%s!%s}{"%(color, attention_list[idx])+"\\strut " + text_list[idx]+"} "
		string += "\n}}}"
		f.write(string+'\n')
		f.write(r'''\end{CJK*}
\end{document}''')

def rescale(input_list):
	the_array = np.asarray(input_list)
	the_max = np.max(the_array)
	the_min = np.min(the_array)
	rescale = (the_array - the_min)/(the_max-the_min)*100
	return rescale.tolist()


def clean_word(word_list):
	new_word_list = []
	for word in word_list:
		for latex_sensitive in ["\\", "%", "&", "^", "#", "_",  "{", "}"]:
			if latex_sensitive in word:
				word = word.replace(latex_sensitive, '\\'+latex_sensitive)
		new_word_list.append(word)
	return new_word_list


if __name__ == '__main__':
	## This is a demo:

	# sent = '''the USS Ronald Reagan - an aircraft carrier docked in Japan - during his tour of the region, vowing to "defeat any attack and meet any use of conventional or nuclear weapons with an overwhelming and effective American response".
# North Korea and the US have ratcheted up tensions in recent weeks and the movement of the strike group had raised the question of a pre-emptive strike by the US.
# On Wednesday, Mr Pence described the country as the "most dangerous and urgent threat to peace and security" in the Asia-Pacific.'''
	# sent = '''??? ?????? ??? ??? ?????? ??? ?????? ?????? ??? ?????? ?????? ?????? ??? ??? Hawaii guitar ??? ??? ?????? Guitar ??? ??? ?????? ??? ????????? ??? ??? ????????? ???
	# ?????? ????????? ??? ??? ??? ?????? ??? ????????? ?????? ?????? ?????? ??? ??? ?????? ?????? ????????? ????????? ??? ??? ??? ??? ????????? ?????? ?????? ?????? ?????? ??? ??? ????????? ??? ?????? ??? ??? ??? ??? ?????? ??? ?????? ?????? ?????? ??? ?????? ?????? ??? ?????? ?????? ???'''
    # ref = "before beginning equine massage it is important to evaluate your horses temperament . learn more about preparing for equine massage with tips from a certified equine sports massage practitioner in this free horse care video ."
    # sent = "so before you begin to work on your horse there are a number of things that you need to keep in mind . you need to think about your horse 's overall condition . you need to think about your horse 's temperament . you need to think about whether your horse is a quote , unquote , thin skinned or a thick skinned horse . you need to consider whether the horse has an illness or an injury . you want to look at the age of your horse . you want to look at your horse 's training schedule , whether they compete or not , whether or not this is a back yard horse that gets ridden on an occasional basis . whether or not the horse has just come from a strenuous competition . whether the horse is coming back from an injury or an illness . you need to basically , before you do anything like this with your horse you need to really know your horse and understand your horse . what kind of touch your horse likes . the kind of grooming that your horse likes . the amount of pressure that they 're comfortable with and your horse 's overall attitude toward life ."
    base_dir = os.path.dirname(os.path.abspath(__file__))
    att_wts_pth = os.path.join(base_dir, 'att_wts')
    dirs = os.listdir(att_wts_pth)
    dirs = [d for d in dirs if os.path.isdir(os.path.join(att_wts_pth, d))]
    for dir in dirs:
        with open(os.path.join(att_wts_pth, dir, 'tran.txt'), 'r') as f:
            sent = f.read()
        words = sent.split(' ')
        word_num = len(words)
        # attention = [(x+1.)/word_num*100 for x in range(word_num)]
        # Load the attention weights
        with open(os.path.join(att_wts_pth, dir, 'h1_att_txt.npy'), 'rb') as f:
            att_fig = np.load(f)
            nans = np.isnan(att_fig)        # NOTE : Check why nan values are being generated
            att_fig[nans] = 0
            attention = list(att_fig.sum(1)*100)[:word_num]
        # import random
        # random.seed(42)
        # random.shuffle(attention)
        color = 'red'
        generate(words, attention, os.path.join(att_wts_pth, dir, "highlight.tex"), color)

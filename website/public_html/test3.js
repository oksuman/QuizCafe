var count = 0;
var gblData = JSON.parse(sessionStorage.getItem('data'));
const inputArr = Array.from({ length: gblData["quiz_count"] }, () => "");

document.getElementById("prev_btn").style.visibility = "hidden";
document.getElementById("next_btn").addEventListener('click', printNextQuiz);
document.getElementById("prev_btn").addEventListener('click', printPrevQuiz);
document.getElementById("checkout").addEventListener('click', result);
document.getElementById("skip").addEventListener('click', skip);
printQuiz();

var answerstr = "";
for (var i = 0; i < gblData["quizzes"][count]["answers"].length; i++) {
	answerstr += gblData["quizzes"][count]["answers"][i].toLowerCase().replace(/ /g,"");
	if (i != (gblData["quizzes"][count]["answers"].length - 1)) { answerstr += ", "; }
}


$(document).on('keypress', function (e) {
	if (e.keyCode == '13') {
		if (count != gblData["quiz_count"] - 1) {
			$('#next_btn').click();
		}	
	}
	if (e.keyCode == '37') {
		$('#prev_btn').click();
	}
	if (e.keyCode == '39') {
		if (count != gblData["quiz_count"] - 1) {
			$('#next_btn').click();
		}
	}
});


function printQuiz() {
	//문제번호
	var str = document.getElementById("quiz_num");
	str.innerHTML = "<span style='font-weight:700;'>"+(count + 1)+"</span> / " + gblData["quiz_count"];
	//주제
	var str1 = document.getElementById("topic");
	str1.innerHTML = gblData["quizzes"][count]["topic"];
	//주제랑 답이 같을 때
	for(var i = 0; i < gblData["quizzes"][count]["answers"].length; i++){
		if(gblData["quizzes"][count]["topic"].toLowerCase().replace(/ /g,"").includes(gblData["quizzes"][count]["answers"][i].toLowerCase().replace(/ /g,"")) == true) {
			var newstr = gblData["quizzes"][count]["topic"].replace(gblData["quizzes"][count]["answers"][i], '&nbsp<span id = "border">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span>');
			str1.innerHTML = newstr;
		}
	}
	
	//문제
	var str2 = document.getElementById("quiz");
	var quiznum = gblData["quizzes"][count]["answers"].length;
	var tag = "";
	var newstr = gblData["quizzes"][count]["sentence"];
	var newstr = newstr.replace(/(\n|\r\n)/g, '<br>');
	var newstr = newstr.replace(/(\t)/g, '<span>&nbsp&nbsp&nbsp&nbsp</span>');

	for (var i = 0; i < quiznum; i++) {
		tag += "<input type=\"text\" autocomplete=\"off\" id=\"check" + i + "\" onfocus=\"this.value=''; return true;\" size =" + (gblData["quizzes"][count]["answers"][i].length + 5) + ">";
		newstr = newstr.replace('[blank]', tag);
		tag = "";
	}
	str2.innerHTML = newstr;
}

function visibleControl() {
	if (count == 0) {
		document.getElementById("next_btn").style.visibility = "visible";
		document.getElementById("prev_btn").style.visibility = "hidden";
	}
	else if (count == gblData["quiz_count"] - 1) {
		document.getElementById("next_btn").style.visibility = "hidden";
		document.getElementById("prev_btn").style.visibility = "visible";
	}
	else {
		document.getElementById("next_btn").style.visibility = "visible";
		document.getElementById("prev_btn").style.visibility = "visible";
	}
}

function result() {
	if (inputArr[count]==""){
		saveAnswer();
	}
	const myanswerArr = JSON.stringify(inputArr);
	sessionStorage.setItem('newdata', JSON.stringify(gblData));
	window.sessionStorage.setItem('myanswer', myanswerArr);
}

function skip() {
	if (count == gblData["quiz_count"] - 1) {
		gblData["quiz_count"]--;
		printPrevQuiz();
		inputArr.splice(count+1, 1);
		gblData["quizzes"].splice(count+1, 1);

		var str = document.getElementById("checkoutS");
		str.innerHTML="";
		str.innerHTML="<button id=\"checkout\" disabled onClick=\"location.href='result.html'\" style = \"width:210px; height:70px;\"><img id=\"checkoutI\" src=\"check.png\" onMouseOver=\"this.src='check_mouseover.png'\" onMouseOut=\"this.src='check.png'\" style=\"width:210px; height:70px; -webkit-user-drag: none;\"></button>"
		var btn_able= document.getElementById("checkout");
		btn_able.disabled = false;	
		document.getElementById("checkout").addEventListener('click', result);
	}

	else if(count == gblData["quiz_count"] -2) {
		gblData["quiz_count"]--;
		count++;
		printQuiz();
		inputArr.splice(count-1, 1);
		gblData["quizzes"].splice(count-1, 1);
		count--;
		var strN = document.getElementById("quiz_num");
		strN.innerHTML = "<span style='font-weight:700;'>"+(count + 1)+"</span> / " + gblData["quiz_count"];

		var str = document.getElementById("checkoutS");
		str.innerHTML="";
		str.innerHTML="<button id=\"checkout\" disabled onClick=\"location.href='result.html'\" style = \"width:210px; height:70px;\"><img id=\"checkoutI\" src=\"check.png\" onMouseOver=\"this.src='check_mouseover.png'\" onMouseOut=\"this.src='check.png'\" style=\"width:210px; height:70px; -webkit-user-drag: none;\"></button>"
		var btn_able= document.getElementById("checkout");
		btn_able.disabled = false;	
		document.getElementById("checkout").addEventListener('click', result);
		visibleControl();
	}

	else {
		inputArr.splice(count, 1);
		gblData["quizzes"].splice(count, 1);
		gblData["quiz_count"]--;
		printQuiz();
		if (gblData["quiz_count"] - 1 == count) {
			visibleControl();
			document.getElementById("checkout").style.display = "block";
		}
	}

	if(gblData["quiz_count"] == 1){
		document.getElementById("next_btn").style.visibility = "hidden";
		
		var str = document.getElementById("trashS");
		str.innerHTML="";
		str.innerHTML="<button id=\"skip\" style=\"width:210px;  height:70px;\"><img id=\"skipI\" src=\"trash_blocked.png\" style=\"width:210px; height:70px; -webkit-user-drag: none;\"></button>"
		var btn_able= document.getElementById("skip");
		btn_able.disabled = true;	

		var str = document.getElementById("checkoutS");
		str.innerHTML="";
		str.innerHTML="<button id=\"checkout\" disabled onClick=\"location.href='result.html'\" style = \"width:210px; height:70px;\"><img id=\"checkoutI\" src=\"check.png\" onMouseOver=\"this.src='check_mouseover.png'\" onMouseOut=\"this.src='check.png'\" style=\"width:210px; height:70px; -webkit-user-drag: none;\"></button>"
		var btn_able= document.getElementById("checkout");
		btn_able.disabled = false;	
		document.getElementById("checkout").addEventListener('click', result);
	}

	
}

function saveAnswer(){
	var quiznum = gblData["quizzes"][count]["answers"].length;
	inputArr[count] ="";
	for (var i = 0; i < quiznum-1; i++) {
		inputArr[count] += document.getElementById('check' + i).value.toLowerCase().replace(/ /g,"") +",";
	}
	inputArr[count] += document.getElementById('check' + (quiznum-1)).value.toLowerCase().replace(/ /g,"")
	console.log(inputArr[count]);
}

function printNextQuiz(){
	saveAnswer();
	count++;
	visibleControl();
	printQuiz();
	
	if(inputArr[count] == ""){//처음간다
		
	}
	else {//돌아왔다가 간다
		var quiznum = gblData["quizzes"][count]["answers"].length;
		var prevanswer = inputArr[count].split(",");
		for (var i = 0; i < quiznum; i++) {
			document.getElementById('check' + i).value = prevanswer[i];
		}	
	}
	if (count == gblData["quiz_count"] - 1) {
		var str = document.getElementById("checkoutS");
		str.innerHTML="";
		str.innerHTML="<button id=\"checkout\" disabled onClick=\"location.href='result.html'\" style = \"width:210px; height:70px;\"><img id=\"checkoutI\" src=\"check.png\" onMouseOver=\"this.src='check_mouseover.png'\" onMouseOut=\"this.src='check.png'\" style=\"width:210px; height:70px; -webkit-user-drag: none;\"></button>"
		var btn_able= document.getElementById("checkout");
		btn_able.disabled = false;
		document.getElementById("checkout").addEventListener('click', result);
	}
}

function printPrevQuiz(){
	saveAnswer();
	count--;
	visibleControl();
	printQuiz();
	if(inputArr[count] == ""){
		
	}
	else {
		var quiznum = gblData["quizzes"][count]["answers"].length;
		var prevanswer = inputArr[count].split(",");
		for (var i = 0; i < quiznum; i++) {
			document.getElementById('check' + i).value = prevanswer[i];
		}
	}
}


var count = 0;
var gblData = JSON.parse(localStorage.getItem('data'));
document.getElementById("prev_btn").style.visibility="hidden";

document.getElementById("next_btn").addEventListener('click',printNextQuiz);
document.getElementById("prev_btn").addEventListener('click',printPrevQuiz);

document.getElementById("quiz_num").innerHTML = "문제 번호 :  " + (count+1);
document.getElementById("topic").innerHTML = "주제 :  " + gblData["quizzes"][count]["topic"];
document.getElementById("quiz").innerHTML = "문제 :  " + gblData["quizzes"][count]["sentence"];

var answerstr ="";

for(var i = 0; i < gblData["quizzes"][count]["answers"].length; i++){
	answerstr += gblData["quizzes"][count]["answers"][i];
	if(i != (gblData["quizzes"][count]["answers"].length-1)) {answerstr += ", ";}
}

document.getElementById("answer").innerHTML = "정답 :  " + answerstr;



function printQuiz(){
    var str = document.getElementById("quiz_num");
	str.innerHTML = "문제 번호 :  " + (count+1);
    var str1 = document.getElementById("topic");
	str1.innerHTML = "주제  :  " + gblData["quizzes"][count]["topic"];
    var str2 = document.getElementById("quiz");
	str2.innerHTML = "문제  :  " + gblData["quizzes"][count]["sentence"];
    var str3 = document.getElementById("answer");
	answerstr ="";
	for(var i = 0; i < gblData["quizzes"][count]["answers"].length; i++){
		answerstr += gblData["quizzes"][count]["answers"][i];
		if(i != (gblData["quizzes"][count]["answers"].length-1)) {answerstr += ", ";}
	}
	str3.innerHTML = "정답 :  " + answerstr;

}

function printNextQuiz(){
    if(count < gblData["quiz_count"] - 1){
	count++;
    printQuiz();
	visibleControl();}
}

function printPrevQuiz(){
    if(count > 0 ){
	count--;
    printQuiz();
	visibleControl();}
}

function checkAnswer() { // 정답 체크
	let answer = document.getElementById('check').value;
	if(answer == ""){
		alert('답을 기입해 주십시오');
	}
	else if(answer == gblData["quizzes"][count]["answers"][0]){
		alert('정답입니다!');
	}
	else{
		document.getElementById('check').value = "";
		alert('정답이 아닙니다!');
	}
}

function visibleControl()
{
  if (count == 0)
  {
	document.getElementById("next_btn").style.visibility="visible";
    document.getElementById("prev_btn").style.visibility="hidden";
  }
  else if (count == gblData["quiz_count"] - 1)
  {
    document.getElementById("next_btn").style.visibility="hidden";
	document.getElementById("prev_btn").style.visibility="visible";
  }
  else
  {
	document.getElementById("next_btn").style.visibility="visible";
	document.getElementById("prev_btn").style.visibility="visible";
  }
}

// 정답 부분 비우고 텍스트필드 넣기
// 답 여러개일때 배열로 갯수만큼 받기, 지금은 [0]만 받는중이다 이말이야
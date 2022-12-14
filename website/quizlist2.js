var gblData = JSON.parse(sessionStorage.getItem('newdata'));
var newData = sessionStorage.getItem('myanswer');
const inputArr = JSON.parse(newData);
const newArr = Array.from({ length: gblData["quiz_count"] }, () => "");

var count = 0;
var correct = 0;
var score = 0;

findAnswer();
printQuizList();

function quiznumOdd() {
    if(gblData["quiz_count"]%2 == 0) return (gblData["quiz_count"]/2);
    else return (gblData["quiz_count"]/2);
}

function findAnswer() {
    checkAnswerStr = "";
    answerstr = "";
    printasnwer= "";
    for (var i = 0; i < gblData["quizzes"][count]["answers"].length; i++) {
        answerstr += gblData["quizzes"][count]["answers"][i].toLowerCase().replace(/ /g,"");
        checkAnswerStr += gblData["quizzes"][count]["answers"][i].toLowerCase().replace(/ /g,"");
        printasnwer += gblData["quizzes"][count]["answers"][i];
        if (i != (gblData["quizzes"][count]["answers"].length - 1)) { answerstr += ","; printasnwer += ",";}
    }
}

function changeSentence() {
    var quiznum = gblData["quizzes"][count]["answers"].length;
    var copy = "";
    var newstr = gblData["quizzes"][count]["sentence"];
    var newstr = newstr.replace(/(\n|\r\n)/g, '<br>');
    var newstr = newstr.replace(/(\t)/g, '<span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span>');
    var newanswerstr = "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp";
    

    for (var i = 0; i < quiznum; i++) {
            copy += "<b id=\"correctanswer\"> " + newanswerstr + " </b>";
            newstr = newstr.replace('[blank]', copy);
            copy = "";
    }
    newArr[count] += newstr;
}

function printQuizList() {
    var tag = "";
    var tag3 = "";
    var str = document.getElementById("quizlist");
    var str3 = document.getElementById("answerlist");
    
    for (var i = 0; i < gblData["quiz_count"]; i++) {
        changeSentence();
        findAnswer();
            tag += "<div style = \"position : relative;\">" + "<\div>" +
            "<div id = \"img2\" style = \"position : absolute;\">" +
            "</div>" +
            "<div>" +
            "<p id=\"quiz_num\"> <font size=\"6\">" + (count + 1) + ". <br></font>"+ "<font size =\"4\">&nbsp&nbsp" + newArr[count] + "</font>" +
            "</div>" +
            "<div>" + "<p><b id=\"answer\"><font-weight:\"600\">주제</b></font><b id = norm>&nbsp&nbsp" + gblData["quizzes"][count]["topic"] + "<br><br></b></p>" + "</div>";
            
            tag3 += "<div style = \"position : relative;\">" + "<\div>" +
            "<div id = \"img2\" style = \"position : absolute;\">" + "</div>" +
            "<div>" + "<p id=\"quiz_num\"> <font size=\"6\">" + (count + 1) + ". </font>"+ "<font size =\"4\">" + printasnwer + "</font>" +"</div>";
             
            count++;
        str.innerHTML = tag;
    }
    str3.innerHTML +=  "<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>" + tag3;

}

$(document).ready(function() {
	$('#savePdf').click(function() { // pdf저장 button id
		document.getElementById("answerlist").style.display = "block";
	    html2canvas($('#pdfDiv')[0]).then(function(canvas) { 
	    var imgData = canvas.toDataURL('image/png');
		imgData.crossOrigin = 'Anonymous';     
	    var imgWidth = 190; // 이미지 가로 길이(mm) / A4 기준 210mm
	    var pageHeight = imgWidth * 1.414;  // 출력 페이지 세로 길이 계산 A4 기준
	    var imgHeight = canvas.height * imgWidth / canvas.width;
	    var heightLeft = imgHeight;
	    var margin = 10; // 출력 페이지 여백설정
	    var doc = new jsPDF('p', 'mm');
	    var position = 0;
	       
	    doc.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
	    heightLeft -= pageHeight;
	         
	    while (heightLeft >= 30) {
	        position = heightLeft - imgHeight -28;
	        doc.addPage();
	        doc.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
	        heightLeft -= pageHeight;
	    }
	    doc.save('quiz_'+getDate()+'.pdf');
        document.getElementById("answerlist").style.display = "none";
	});
	});
})

function getDate() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth()+1
    var day = date.getDate();
    if(month < 10){
        month = "0"+month;
    }
    if(day < 10){
        day = "0"+day;
    }
    var date = year+""+month+""+day;
    return date;
}

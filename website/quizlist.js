var gblData = JSON.parse(sessionStorage.getItem('newdata'));
var newData = sessionStorage.getItem('myanswer');
const inputArr = JSON.parse(newData);
const newArr = Array.from({ length: gblData["quiz_count"] }, () => "");

var count = 0;
var correct = 0;
var score = 0;

findAnswer();
printQuizList();
makeScore();

function findAnswer() {
    checkAnswerStr = "";
    answerstr = "";
    printasnwer= "";
    for (var i = 0; i < gblData["quizzes"][count]["answers"].length; i++) {
        answerstr += gblData["quizzes"][count]["answers"][i].toLowerCase().replace(/ /g,"");
        checkAnswerStr += gblData["quizzes"][count]["answers"][i].toLowerCase().replace(/ /g,"");
        printasnwer += gblData["quizzes"][count]["answers"][i];
        if (i != (gblData["quizzes"][count]["answers"].length - 1)) { answerstr += ","; printasnwer += ", ";}
    }
}

function changeSentence() {
    var quiznum = gblData["quizzes"][count]["answers"].length;
    var copy = "";
    var newstr = gblData["quizzes"][count]["sentence"];
    var newstr = newstr.replace(/(\n|\r\n)/g, '<br>');
    var newstr = newstr.replace(/(\t)/g, '<span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span>');
    var newanswerstr = inputArr[count].toLowerCase().replace(/ /g,"").split(",");
    var newanswerstr2 = inputArr[count].split(",");

    var str = answerstr.split(",");

    for (var i = 0; i < quiznum; i++) {
        if (newanswerstr[i] == str[i]) {
            copy += "<b id=\"correctanswer\">" + newanswerstr2[i] + " </b>";
            newstr = newstr.replace('[blank]', copy);
            copy = "";
        }
        else {
            if(newanswerstr[i] == ""){
                copy += "<b id=\"wronganswer\"><span><font size =\"3px\";>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</font></span></b>";
                newstr = newstr.replace('[blank]', copy);
                copy = "";
            }
            else {
                copy += "<b id=\"wronganswer\">" + newanswerstr2[i] + "</b>";
                newstr = newstr.replace('[blank]', copy);
                copy = "";
            }
        }
    }
    newArr[count] += newstr;
}

function printQuizList() {
    var tag = "";
    var str = document.getElementById("quizlist");

    for (var i = 0; i <gblData["quiz_count"]; i++) {
        
        findAnswer();
        changeSentence();
            
            if (answerstr == inputArr[count].toLowerCase().replace(/ /g,""))   {
                tag += "<div style = \"position : relative;\">" + "<\div>" +
                "<div id = \"img\" style = \"position : absolute;\">" +
                "<img src=\"correct.png\" style=\"width:90px; height:90px; -webkit-user-drag: none;\"></img>" +
                "</div>" +
                "<div>" + 
                "<p id=\"quiz_num\"> <font size=\"6\">" + (count + 1) + ". <br></font>&nbsp&nbsp"+ newArr[count] +
                "</div>" + 
                "<div>" + "<p><b id=\"answer\"><font-weight:\"600\">주제</b></font><b id = norm>&nbsp&nbsp" + gblData["quizzes"][count]["topic"] + "</b></p>" + "</div>" +
                "<div>" + "<p><b id=\"answer\"><font-weight:\"600\">정답</b></font><b id = norm>&nbsp&nbsp" + printasnwer + "</b></p>" + "</div>"+
                "<div>" + "<p><b id=\"answer\"><font-weight:\"600\">출처</b></font><b id = norm>&nbsp&nbsp"+gblData["quizzes"][count]["source"] + "</b></p> </div>";
                count++;
                correct++;
            }
            else {
                tag += "<div style = \"position : relative;\">" + "<\div>" +
                    "<div id = \"img2\" style = \"position : absolute;\">" +
                    "<img src=\"incorrect.png\" style=\"width:90px; height:90px; -webkit-user-drag: none;\"></img>" +
                    "</div>" +
                    "<div>" +
                    "<p id=\"quiz_num\"> <font size=\"6\">" + (count + 1) + ". <br></font>&nbsp&nbsp"+ newArr[count] +
                    "</div>" +
                    "<div>" + "<p><b id=\"answer\"><font-weight:\"600\">주제</b></font><b id = norm>&nbsp&nbsp" + gblData["quizzes"][count]["topic"] + "</b></p>" + "</div>" +
                    "<div>" + "<p><b id=\"answer\"><font-weight:\"600\">정답</b></font><b id = norm>&nbsp&nbsp" + printasnwer + "</b></p>" + "</div>"+
                    "<div>" + "<p><b id=\"answer\"><font-weight:\"600\">출처</b></font><b id = norm>&nbsp&nbsp"+gblData["quizzes"][count]["source"] + "</b></p> </div>";
                count++;
            }
            str.innerHTML = tag;
        }
        
    
}

function makeScore() {
    var str = document.getElementById("score");
    str.innerHTML += "<font style=\"color:red\">"+ correct + "</font>" + " / " + gblData["quiz_count"];
}

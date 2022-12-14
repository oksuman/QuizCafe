var fileList = []; //파일 정보를 담아 둘 배열
var fileNum = 0;
var deleteCount = 0;

$(function () {
    // 파일 선택으로 파일 입력
    $(document).on("change", "#plus", function () {
        document.getElementById("notpdf").style.display = "none";
        document.getElementById("manypdf").style.display = "none";
        var fileInput = document.getElementById("plus");
        var files = fileInput.files;
        if(files.length < 6){
            if(fileList.length + files.length-fileList.filter(element => null === element).length< 6){
                if (files != null && files != undefined) {
                    document.getElementById("plusB").style.display = "block";
                    document.getElementById("uploadB").style.display = "block";
                    document.getElementById("inborder").style.display = "none";
                    document.getElementById("notpdf").style.display = "none";
                    document.getElementById("manypdf").style.display = "none";

                    var tag = "";
                    for (i = 0; i < files.length; i++) {
                        var f = files[i];
                        fileList.push(f);
                        var fileName = f.name;
                        tag +=
                            "<div class=\"fileList\" id=\"num_" + fileNum + "\">" +
                            "<span class='fileName'>" + fileName + "</span>" +
                            "<span id =\"deleteB\"><button type=\"button\" class=\"deleteFile\" id=\"delete\">×</button></span>" +
                            "</div>";
                        fileNum++;
                    }
                    $("#fileDrop").append(tag);
        
                    var input = document.getElementById("plus");
                    input.value = null;
                }
            }
            else{
                document.getElementById("manypdf").style.display = "block";
            }
        }
        else{
            document.getElementById("manypdf").style.display = "block";
        }
    });

    // 드래그로 파일 입력
    $("#fileDrop").on("dragenter", function (e) {
        e.preventDefault();
        e.stopPropagation();
    }).on("dragover", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).css("background-color", "#F0F8FF");
    }).on("dragleave", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).css("background-color", "#FFF");
    }).on("drop", function (e) {
        e.preventDefault();
        document.getElementById("notpdf").style.display = "none";
        document.getElementById("manypdf").style.display = "none";
        var files = e.originalEvent.dataTransfer.files;
        for(var i = 0; i < files.length; i++){
            if(files[i].name.includes(".pdf") == false) {
                $(this).css("background-color", "#FFF");
                document.getElementById("notpdf").style.display = "block";
                return 0;
            }
        }
        if(files.length < 6){
            if(fileList.length + files.length-fileList.filter(element => null === element).length< 6){
                if (files != null && files != undefined) {
                    document.getElementById("plusB").style.display = "block";
                    document.getElementById("uploadB").style.display = "block";
                    document.getElementById("inborder").style.display = "none";
                    document.getElementById("notpdf").style.display = "none";
                    document.getElementById("manypdf").style.display = "none";
                    var tag = "";
                    for (i = 0; i < files.length; i++) {
                        var f = files[i];
                        fileList.push(f);
                        var fileName = f.name;
                        tag +=
                            "<div class=\"fileList\" id=\"num_" + fileNum + "\">" +
                            "<span class='fileName'>" + fileName + "</span>" +
                            "<span id =\"deleteB\"><button type=\"button\" class=\"deleteFile\" id=\"delete\">×</button></span>"+
                            "</div>";
                        fileNum++;
                    }
                    $(this).append(tag);
                }
            }
            else{
                document.getElementById("manypdf").style.display = "block";
            }
        }
        else{
            document.getElementById("manypdf").style.display = "block";
        }
        $(this).css("background-color", "#FFF");
    });

    // 파일 제거
    $(document).on("click", ".deleteFile", function () {
        deleteCount++;
        var fileIndex = $("button").index(this);
        console.log(fileIndex);
        // fileList.splice(fileIndex, 1);
        fileList[fileIndex] = null;
        document.getElementById("num_" + fileIndex).style.display = "none";
        document.getElementById("notpdf").style.display = "none";
        document.getElementById("manypdf").style.display = "none";
        console.log(fileList);
        if (deleteCount == fileList.length) {
            document.getElementById("inborder").style.display = "block";
            document.getElementById("plusB").style.display = "none";
            document.getElementById("uploadB").style.display = "none";
            document.getElementById("notpdf").style.display = "none";
            document.getElementById("manypdf").style.display = "none";
        }
    });

    // 업로드
    $(document).on("click", "#upload", function () {
        var formData = new FormData($("#fileForm")[0]);
        if (fileList.length > 0) {
            for (var i = 0; i < fileList.length; i++) {
                if (fileList[i] != null) {
                    formData.append("files", fileList[i]);
                }
            }
        }

        $("#div_load_image").show();
        $(".fileList").css("display","none");
        document.getElementById("plusB").style.display = "none";
        document.getElementById("uploadB").style.display = "none";
        document.getElementById("loading").style.display = "block";
        document.getElementById("notpdf").style.display = "none";
        document.getElementById("manypdf").style.display = "none";

        $.ajax({
            url: "http://34.64.133.122:1515/api/v1/quiz",
            data: formData,
            type: 'POST',
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            dataType: 'json',
            cache: false,
            success: function (res) {
                $("#div_load_image").hide();
                console.log(res)
                if (res["quiz_count"] != 0) {
                    document.getElementById("loading").style.display = "none";
                    document.getElementById("success").style.display = "block";
                    document.getElementById("quizNum").style.display = "block";
                    document.getElementById("quizNum").innerHTML = res["quiz_count"] + "개의 문제가 생성되었습니다";
                    document.getElementById("startB").style.display = "block";
                    sessionStorage.setItem('data', JSON.stringify(res));
                }
                else {
                    document.getElementById("loading").style.display = "none";
                    document.getElementById("fail").style.display = "block";
                    document.getElementById("quizNum").style.display = "block";
                    document.getElementById("quizNum").innerHTML = "문제 생성에 실패했습니다";
                    document.getElementById("reuploadB").style.display = "block";
                }

            }, error: function (res) {
                $("#div_load_image").hide();
                document.getElementById("loading").style.display = "none";
                document.getElementById("fail").style.display = "block";
                document.getElementById("quizNum").style.display = "block";
                document.getElementById("quizNum").innerHTML = "문제 생성에 실패했습니다";
                document.getElementById("reuploadB").style.display = "block";
            }
        });
    });
});





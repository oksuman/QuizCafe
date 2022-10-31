var fileList = []; //파일 정보를 담아 둘 배열
$(function(){

    //드래그로 파일 입력
    $("#fileDrop").on("dragenter", function(e){
        e.preventDefault();
        e.stopPropagation();
    }).on("dragover", function(e){
        e.preventDefault();
        e.stopPropagation();
        $(this).css("background-color", "#FFD8D8");
    }).on("dragleave", function(e){
        e.preventDefault();
        e.stopPropagation();
        $(this).css("background-color", "#FFF");
    }).on("drop", function(e){
        e.preventDefault();

        var files = e.originalEvent.dataTransfer.files;
        if(files != null && files != undefined){
            var tag = "";
            for(i=0; i<files.length; i++){
                var f = files[i];
                fileList.push(f);
                var fileName = f.name;
                tag += 
                        "<div class='fileList'>" +
                            "<span class='fileName'>"+fileName+"</span>" +
                            "<span class='clear'></span>" +
                        "</div>";
            }
            $(this).append(tag);
        }

        $(this).css("background-color", "#FFF");
    });

    //업로드
    $(document).on("click", "#upload", function(){
        var formData = new FormData($("#fileForm")[0]);
        if(fileList.length > 0){
            fileList.forEach(function(f){
                formData.append("files", f);
            });
        }         

        $.ajax({
            url : "https://f69d-219-255-207-61.jp.ngrok.io/api/v1/quiz",
            data : formData,
            type:'POST',
            enctype:'multipart/form-data',
            processData:false,
            contentType:false,
            dataType:'json',
            cache:false,
            success:function(res){
                console.log(res)
                alert(res["quiz_count"] + "개의 문제가 생성되었습니다");
                localStorage.setItem('data', JSON.stringify(res));
            },error:function(res){
                alert("저장에 실패했습니다.");
            }
        });
    });
});


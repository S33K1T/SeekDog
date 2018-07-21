$(document).ready(function () {
    $(".query-btn").click(function () {
        let query_num = $("input[type=checkbox]:checked").length;
        for (let i = 0; i < query_num; i++) {
            // console.log($("input[type=checkbox]:checked")[i].id);
            let checkId = $("input[type=checkbox]:checked")[i].id;
            switch (checkId) {
                case 'checkbox1':
                    whois();
                    break;
                case 'checkbox2':
                    dns();
                    break;
                case 'checkbox3':
                    portScan();
                    break;
                case 'checkbox4':
                    webFinger();
                    break;
                case 'checkbox6':
                    robots();
                    break;
                case 'checkbox7':
                    linkCheck();
                    break;
                case 'checkbox8':
                    routerPop();
                    break;
                case 'checkbox9':
                    reverseIp();
                    break;
                default:
                    break;
            }
        }
    });
});

function change(myid, mode) {
    document.getElementById(myid).style.display = mode;
    if (mode === 'block') {
        // 设置下拉菜单所在 div 的边框
        document.getElementById(myid).style.border = "1px solid #eee";
        document.getElementById(myid).style.borderTop = "none";
        // 设置鼠标划过的 li 的边框及背景颜色
        document.getElementById(myid).parentNode.backgroundColor = "#fff";
        document.getElementById(myid).parentNode.border = "1px solid #eee";
        document.getElementById(myid).parentNode.borderBottom = "none";
    }
    else {
        // 不显示下拉菜单，鼠标划过的 li 的边框及背景颜色
        document.getElementById(myid).parentNode.backgroundColor = "";
        document.getElementById(myid).parentNode.border = "";
    }
}

function checkAll() {
    var all = document.getElementById('all');//获取到点击全选的那个复选框的id
    var one = document.getElementsByName('checkname[]');//获取到复选框的名称
    if (all.checked == true) {//因为获得的是数组，所以要循环 为每一个checked赋值
        for (var i = 0; i < one.length; i++) {
            one[i].checked = true;
        }

    } else {
        for (var j = 0; j < one.length; j++) {
            one[j].checked = false;
        }
    }
}

function whois() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/;
    var result = document.getElementById('result1');
    var data = url.value;
    if (url.value.indexOf("http://") != -1) {
        data = url.value.substring(7);
    }
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;";
        $.ajax({
            url: "./ajax-whois/",
            method: "POST",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            success: function (result) {
                $("#result1").html("");
                $("#result1").css("height", "650px");
                $("#result1").append("<iframe src='./output-whois/' style='width:100%;height:100%;'></iframe>");
            },
            error: function (error) {
                alert(error);
            }
        })
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}

function dns() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/;
    var result = document.getElementById('result2');
    var data = url.value;
    $("#result2").html("DNS查询中，请稍后...");
    if (url.value.indexOf("http://") != -1) {
        data = url.value.substring(7);
    }
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;";
        $.ajax({
            type: "POST",
            url: "./ajax-DnsInfo/",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            error: function (e) {
                $("#result2").html("DNS查询出错")
            },
            success: function (result) {
                $("#result2").html("");
                var line = "";
                for (i = 0; i < result.length; i++) {
                    if (result[i] != '\n') {
                        line += result[i];
                    } else {
                        $("#result2").append("<p>" + line + "</p>");
                        line = "";
                    }
                }
            }
        })
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}

function portScan() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/
    var result = document.getElementById('result3');
    var data = url.value;
    $("#result3").html("端口检测中，请稍后...");
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;";
        $.ajax({
            type: "POST",
            url: "./ajax-portScan/",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            error: function (error) {
                $("#result3").html("端口扫描出错!")
            },
            success: function (result) {
                $("#result3").html("");
                jstr = JSON.parse(result)
                $("#result3").append("<div style=\"color:\"green\";\">");
                for (i = 0; i < jstr.length; i++) {
                    $("#result3").append(jstr[i]['ip'] + " : " + jstr[i]['port'][0] + "<br>");
                }
                $("#result3").append("</div>");
            }
        });
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}

function webFinger() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/;
    var result = document.getElementById('result4');
    var data = url.value;
    $("#result4").html("CMS查询中，请稍后...");
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;";
        $.ajax({
            type: "POST",
            url: "./ajax-webFinger/",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            error: function (error) {
                $("#result4").html("CMS查询失败!");
            },
            success: function (result) {
                $("#result4").html("");
                jstr = JSON.parse(result);
                $("#result4").append("<p>" + jstr[0] + "</p>");
                $("#result4").append("<p>" + jstr[1] + "</p>");
                $("#result4").append("<p>" + jstr[2] + "</p>");
            }
        });
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}

function robots() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/
    var result = document.getElementById('result5');
    var data = url.value;
    if (url.value.indexOf("http://") != -1) {
        data = url.value.substring(7);
    }
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;"
        $("#result5").html("robots文件枚举中，请稍后...")
        $.ajax({
            type: "POST",
            url: "./ajax-robots/",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            error: function (error) {
                $("#result5").html("查询失败，请重试")
            },
            success: function (result) {
                $("#result5").html("");
                var str = "";
                for (i = 0; i < result.length; i++) {
                    if (result[i] != '\n') {
                        str += result[i];
                    } else {
                        $("#result5").append("<p>" + str + "</p>");
                        str = "";
                    }
                }
            }
        })
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}

function linkCheck() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/;
    var result = document.getElementById('result6');
    var data = url.value;
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;";
        $("#result6").html("链接检测中，请稍后...");
        $.ajax({
            type: "POST",
            url: "./ajax-linkCheck/",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            error: function (error) {
                $("#result6").html("链接检测失败，请重试!")
            },
            success: function (result) {
                $("#result6").html("");
                var _url = "";
                if (result == "no links found") {
                    $("#result6").append("<p>" + result + "</p>");
                    return;
                }
                for (i = 0; i < result.length; i++) {
                    if (result[i] != '\n') {
                        _url += result[i]
                    } else {
                        $("#result6").append("<p>" + _url + "</p>");
                        _url = "";
                    }
                }
            }
        })
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}

function routerPop() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/;
    var result = document.getElementById('result7');
    var data = url.value;
    if (url.value.indexOf("http://") != -1) {
        data = url.value.substring(7);
    }
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;"
        $("#result7").html("路由跳板检测中，大约5-10秒，请稍后....");
        $.ajax({
            type: "POST",
            url: "./ajax-routerPop/",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            error: function (error) {
                $("#result7").html("路由跳点检测失败，请重试");
            },
            success: function (result) {
                $("#result7").html("");
                var line = "";
                for (i = 0; i < result.length; i++) {
                    if (result[i] != '\n') {
                        if (result[i] == ' ') {
                            line += "&nbsp;";
                        } else {
                            line += result[i];
                        }
                    } else {
                        $("#result7").append("<p>" + line + "</p>");
                        line = "";
                    }
                }
            }
        })
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}

function reverseIp() {
    var url = document.getElementById('url');
    var reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/
    var result = document.getElementById('result8');
    var data = url.value;
    if (url.value.indexOf("http://") != -1) {
        data = url.value.substring(7);
    }
    if (reg.test(url.value)) {
        result.style.display = "block";
        url.style.cssText = "border:1px solid green;";
        $("#result8").html("反向ip查询中，请稍后...");
        $.ajax({
            type: "POST",
            url: "./ajax-ipLookup/",
            data: {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 'url': data},
            error: function (error) {
                $("#result8").html("Url出错，查询失败")
            },
            success: function (result) {
                var _url = "";
                for (i = 0; i < result.length; i++) {
                    if (result[i] != '\n') {
                        _url += result[i]
                    } else {
                        $("#result8").append("<p>" + _url + "</p>");
                        _url = ""
                    }
                }
            }
        })
    }
    else {
        url.style.cssText = "border:1px solid red"
    }
}
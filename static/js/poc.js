$(document).ready(function () {
    $(".page1").parent().addClass("bg-blue");
    for (let i = 1; i <= $(".pageNum").val(); i++) {
        $(".page" + i).click((function (n) {
            return function () {
                // alert(n);
                let start = (n - 1) * 5;
                $.ajax({
                    type: "GET",
                    url: "../ajax-POC/?start=" + start,
                    success: function (result) {
                        do_success(n, result);
                        tickAll();
                    }
                })
            }
        })(i))
    }
    $(".next-page").click(function () {
        let n = getCurrentPage() + 1;
        let start = (n - 1) * 5;
        if (n > $(".pageNum").val()) {
            return;
        }
        $.ajax({
            type: "GET",
            url: "../ajax-POC/?start=" + start,
            success: function (result) {
                do_success(n, result);
                tickAll();
            }
        })
    });
    $(".poc-search-btn").click(searchKeywords);
    $(".all-tick").click(tickAll);
    $(".poc-url-btn").click(multiplyVerifyPoc);
});

var keywords;

function searchKeywords() {
    $(".poc-list-tbl tr").css("display", "table-row");
    $(".all-tick")[0].checked = false;
    $.ajax({
        type: "POST",
        url: "../ajax-POC/",
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            "type": "search",
            "keywords": $(".poc-search-text").val()
        },
        error: function () {
            alert(-1)
        },
        success: function (result) {
            keywords = result;
            do_success(1, result);
            showDetail($(".poc-search-text").val(), result);
            changeToSearchPaginator()
        }
    })
}

function tickAll() {
    if ($(".all-tick")[0].checked == true) {
        for (let i = 0; i < 5; i++) {
            $("input:checkbox")[i].checked = true;
        }
    } else {
        for (let i = 0; i < 5; i++) {
            $("input:checkbox")[i].checked = false;
        }
    }
}

function getCurrentPage() {
    for (let i = 1; i <= $(".pageNum").val(); i++) {
        if ($(".page" + i).parent().hasClass("bg-blue")) {
            return i;
        }
    }
}

function goToPage(n) {
    let start = (parseInt(n) - 1) * 5;
    $.ajax({
        type: "GET",
        url: "../ajax-POC/?start=" + start,
        success: function (result) {
            do_success(n, result);
        }
    })
}

function do_success(n, result) {
    var jstr = JSON.parse(result);
    // input tick_num
    for (let i = 1; i <= 5; i++) {
        $(".tick" + (i - 1)).html("<input type=\"checkbox\" name=\"check\">" + ((n - 1) * 5 + i));
    }
    // show poc_list
    for (let i = 0; i < (jstr.length < 5 ? jstr.length : 5); i++) {
        if ((i + 1) != n) {
            $(".page" + (i + 1)).parent().removeClass("bg-blue");
        } else {
            $(".page" + n).parent().addClass("bg-blue");
        }

        for (let j = 0; j < 3; j++) {
            $(".list_" + i + "_" + j).html(jstr[i][j]);
        }
    }
    // hide not exist one
    if (keywords != undefined) {
        for (let i = jstr.length + 1; i <= 5; i++) {
            for (let j = 1; j <= 3; j++) {
                $(".list_" + (i - 1) + "_" + (j - 1)).parent().css("display", "none");
            }
        }
    }
}

function showDetail(key, result) {
    $(".detai").html("关键字：" + key + ", 共计：" + JSON.parse(result).length + "条");
}

function changeToSearchPaginator() {
    $(".paginator").removeClass("show").addClass("hidden");
    $(".paginator-search").removeClass("hidden").addClass("show");
    let jstr = JSON.parse(keywords);
    let len = jstr.length;
    $(".paginator-search").html("");
    for (let i = 0; i < Math.ceil(len / 5); i++) {
        let index = len > ((i + 1) * 5) ? ((i + 1) * 5) : len;
        $(".paginator-search").append("<span><a href=\"javascript:void(0)\" class=\"search-page" + i + "\">" + (i + 1) + "</a></span>");
        $(".search-page" + i).click(function () {
            for (let p = i * 5; p < index; p++) {
                $(".tick" + (p - i * 5)).html("<input type=\"checkbox\" name=\"check\">" + (p + 1));
                for (let q = 0; q < 3; q++) {
                    $(".list_" + (p - i * 5) + "_" + q).html(jstr[p][q]);
                }
            }
            for (let p = index; p < (len < ((i + 1) * 5) ? ((i + 1) * 5) : len); p++) {
                $(".tick" + (p - i * 5)).html("");
                for (let q = 0; q < 3; q++) {
                    $(".list_" + (p - i * 5) + "_" + q).html("");
                }
            }
        })
    }

}

function verifyPoc(pocName, url) {
    $.ajax({
        type: "POST",
        url: "../ajax-POC/",
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'type': "scan",
            'url': $(".poc-url-text").val(),
            "poc_name": pocName
        },
        error: function () {
            $(".result-row").append("<tr><td>" + pocName + "</td><td>None</td><td>Not Found</td></tr>");
        },
        success: function (result) {
            let jstr = JSON.parse(result);
            $(".result-row").append("<tr><td>" + jstr[0] + "</td>" + "<td>" + jstr[1] + "</td>" + "<td>" + jstr[2] + "</td></tr>");
        }
    })
}

function progressBar(n, all) {
    one = 250/all;
    $(".percent").html(n/all*100 + "%");
    $(".in-bar").css("width",one*n+"px");
}

function multiplyVerifyPoc() {
    url = $(".poc-url-text").val();
    $(".poc-progress-bar").css("display", "flex");
    $(".poc-list-tbl").css("display", "table");
    if (keywords != undefined) {    // 有关键字的检测
        if ($(".all-tick")[0].checked == true) {
            jstr = JSON.parse(keywords);
            for (let i = 0; i < jstr.length; i++) {
                verifyPoc(jstr[i][0], url);
                progressBar(i+1, jstr.length);
            }
        } else {
            len = $("input[type='checkbox']:checked").parent().next().length;
            for (let i = 0; i < len; i++) {
                pocName = $("input[type='checkbox']:checked").parent().next()[i].innerHTML;
                verifyPoc(pocName, url);
                progressBar(i+1, len);
            }
        }
    } else {    // 普通检测
        len = $("input[type='checkbox']:checked:not(.all-tick)").parent().next().length;
        for (let i = 0; i < len; i++) {
            pocName = $("input[type='checkbox']:checked").parent().next()[i].innerHTML;
            verifyPoc(pocName, url);
            progressBar(i+1, len);
        }
    }
}
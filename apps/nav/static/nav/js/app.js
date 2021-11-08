let edit_flag = localStorage.getItem("edit_flag") || "0";
let dataStr = localStorage.getItem("dataStr") || excludeListLast;
localStorage.setItem("dataStr", dataStr);
let data = dataStr.length > 0 ? dataStr.split(",") : [];
const adds = Array.from($(".edit-mode .add"));
const deletes = Array.from($(".edit-mode .delete"));
const edit_span = $(".edit");

function disableLink(a) {
	$(a).attr('onclick', "return false");
	setTimeout(function () {
		$(a).removeAttr("onclick");
	}, 100);
}
function markExclude(a) {
	$(a).css("background-color", "gray"); //添加标记
}
function markInclude(a) {
	$(a).css("background-color", "white");
}
function exclude(e) {
	let a = $(e.target).parent().parent().parent().parent()[0]
	let add_i = $($(a).find(".add")[0]).find("i")[0] //.add 中的i
	let delete_i = $($(a).find(".delete")[0]).find("i")[0] //.delete中的i
	disableLink(a); markExclude(a);//禁止跳转，并标记为排除
	$(add_i).css("display", "inline-block"); $(delete_i).css("display", "none");
	data.push($(a).find("abbr")[0].title);
	localStorage.setItem("dataStr", data); dataStr = localStorage.getItem("dataStr");
}
function include(e) {
	let a = $(e.target).parent().parent().parent().parent()[0];
	let add_i = $($(a).find(".add")[0]).find("i")[0] //.add 中的i
	let delete_i = $($(a).find(".delete")[0]).find("i")[0] //.delete中的i
	disableLink(a); markInclude(a); //禁止跳转，并标记为包含
	$(delete_i).css("display", "inline-block"); $(add_i).css("display", "none");
	data.pop($(a).find("abbr")[0].title);
	localStorage.setItem("dataStr", data); dataStr = localStorage.getItem("dataStr");
}
deletes.forEach(element => {
	element.addEventListener("click", exclude)
});
adds.forEach(element => {
	element.addEventListener("click", include)
});

function startEdit() {
	edit_span.text(" 确定");
	const edit_mode_items = Array.from($(".edit-mode"));
	const display_mode_items = Array.from($(".display-mode"));
	edit_mode_items.forEach(item => $(item).css("display", "grid"));
	display_mode_items.forEach(item => $(item).css("display", "none"));
	deletes.forEach(element => $(element).children("i").css("display", "inline-block"));
	data.forEach(pk => {
		let abbr = $("#main").find(`abbr[title="${pk}"]`)[0];
		let a = $(abbr).parent().parent().parent()[0];
		markExclude(a);//标记为排除
		let add_i = $($(a).find(".add")[0]).find("i")[0] //.add 中的i
		let delete_i = $($(a).find(".delete")[0]).find("i")[0] //.delete中的i
		$(add_i).css("display", "inline-block"); $(delete_i).css("display", "none");
	})
}

function toggleEdit(e) {
	if (edit_flag == "0") {
		edit_flag = "1";
		localStorage.setItem("edit_flag", edit_flag);
		startEdit();
	} else {
		edit_flag = "0";
		localStorage.setItem("edit_flag", edit_flag);
		$.ajax({
			url: "config/",
			data: {
				"excludeList": dataStr,
				csrfmiddlewaretoken: csrfToken,
			},
			type: "POST",
			dataType: "json",
			success: function (data) {
				setTimeout(function () {
					localStorage.removeItem('dataStr');
					location.reload();
				}, 100)
			}
		});
	}
}
edit_span.on("click", toggleEdit);

if (edit_flag == "1") {
	startEdit();
}
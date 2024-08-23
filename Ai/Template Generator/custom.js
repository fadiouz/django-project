// document.addEventListener('DOMContentLoaded', function () {

// 	document.querySelector('#btn-one').addEventListener('click', function () {
// 		html2canvas(document.querySelector('#content')).then((canvas) => {
// 			let base64image = canvas.toDataURL('image/png');

// 			let pdfWidth = 395.28;
// 			let pdfHeight = 841.89;

// 			let pdf = new jsPDF('p', 'px', [pdfWidth, pdfHeight]);
// 			let imageWidth = pdfWidth - 30;
// 			let imageHeight = (imageWidth * canvas.height) / canvas.width

// 			pdf.addImage(base64image, 'PNG', 15, 15, imageWidth, imageHeight);
// 			pdf.save('pdf');
// 		});
// 	});
// });


document.addEventListener('DOMContentLoaded', function () {
	document.querySelector('#btn-one').addEventListener('click', function () {
		html2canvas(document.querySelector('#content')).then((canvas) => {
			let base64image = canvas.toDataURL('image/png');

			let pdfWidth = 24 * 37.8;
			let pdfHeight = 34 * 37.8;

			let pdf = new jsPDF('p', 'px', [pdfWidth, pdfHeight], true);

			let imageWidth = pdfWidth - 30;
			let imageHeight = (imageWidth * canvas.height) / canvas.width;

			pdf.addImage(base64image, 'PNG', 15, 15, imageWidth, imageHeight, '', 'FAST');

			pdf.save('pdf');
		});
	});
});


function After_selection() {
	var content = document.getElementById("content");
	content.classList.add("show");
	content.classList.remove("hide");

	var buttons = document.getElementById("buttons");
	buttons.classList.add("show");
	buttons.classList.remove("hide");

	var imgSelect = document.getElementById("img_select");
	imgSelect.classList.add("hide");
	imgSelect.classList.remove("show");
}


function Before_selection() {
	var content = document.getElementById("content");
	content.classList.add("hide");
	content.classList.remove("show");

	var buttons = document.getElementById("buttons");
	buttons.classList.add("hide");
	buttons.classList.remove("show");

	var imgSelect = document.getElementById("img_select");
	imgSelect.classList.add("show");
	imgSelect.classList.remove("hide");
}

function createQuestions(num_of_elements) {

	// var num_of_elements = document.getElementById("numInput").value;
	num_of_elements = parseInt(num_of_elements);
	After_selection()

	if (!isNaN(num_of_elements) && num_of_elements > 0) {
		var quastionElement = document.getElementById("quastion");
		quastionElement.innerHTML = "";

		var main_div = createCircleContainer("row");
		quastionElement.appendChild(main_div);



		if (num_of_elements < 26) {
			var left_div = createCircleContainer("col-md left_div");
			main_div.appendChild(left_div);

			var left_ul = createCircleContainerUl("left");
			left_div.appendChild(left_ul);
		}

		else if (num_of_elements < 51) {
			var left_div = createCircleContainer("col-md-6 left_div");
			main_div.appendChild(left_div);

			var center_div = createCircleContainer("col-md-6 center_div");
			main_div.appendChild(center_div);

			var left_ul = createCircleContainerUl("left");
			left_div.appendChild(left_ul);

			var center_ul = createCircleContainerUl("center");
			center_div.appendChild(center_ul);
		}


		else if (num_of_elements < 76) {
			var left_div = createCircleContainer("col-md-4 left_div");
			main_div.appendChild(left_div);

			var center_div = createCircleContainer("col-md-4 center_div");
			main_div.appendChild(center_div);

			var center2_div = createCircleContainer("col-md-4 center2_div");
			main_div.appendChild(center2_div);

			var left_ul = createCircleContainerUl("left");
			left_div.appendChild(left_ul);

			var center_ul = createCircleContainerUl("center");
			center_div.appendChild(center_ul);

			var center2_ul = createCircleContainerUl("center2");
			center2_div.appendChild(center2_ul);
		}

		else {
			var left_div = createCircleContainer("col-md-3 left_div");
			main_div.appendChild(left_div);

			var center_div = createCircleContainer("col-md-3 center_div");
			main_div.appendChild(center_div);

			var center2_div = createCircleContainer("col-md-3 center2_div");
			main_div.appendChild(center2_div);

			var right_div = createCircleContainer("col-md-3 right_div");
			main_div.appendChild(right_div);


			var left_ul = createCircleContainerUl("left");
			left_div.appendChild(left_ul);

			var center_ul = createCircleContainerUl("center");
			center_div.appendChild(center_ul);

			var center2_ul = createCircleContainerUl("center2");
			center2_div.appendChild(center2_ul);

			var right_ul = createCircleContainerUl("right");
			right_div.appendChild(right_ul);

		}

		function createCircleContainer(className) {
			var circleContainer = document.createElement("div");
			circleContainer.className = className;
			return circleContainer;
		}


		function createCircleContainerUl(className) {
			var circleContainerul = document.createElement("li");
			circleContainerul.className = className;
			return circleContainerul;
		}

		function createNumOfQuastion(i) {
			var num_of_quastion = document.createElement("div");
			num_of_quastion.className = "num_of_quastion";
			num_of_quastion.innerHTML = "<span>" + i + "_</span>";
			return num_of_quastion;
		}

		function createCircle(letters) {
			var circle = document.createElement("div");
			circle.className = "circle";
			var letter = document.createElement("span");
			letter.className = "letter";
			letter.innerHTML = letters;
			circle.appendChild(letter);
			return circle;
		}

		var columnClass;
		for (var i = 1; i <= num_of_elements; i++) {
			if (i < 26) {
				columnClass = left_ul;
			} else if (i < 51) {
				columnClass = center_ul;
			}
			else if (i < 76) {
				columnClass = center2_ul;
			} else if (i < 101) {
				columnClass = right_ul;
			}
			else {
				return false;
			}

			var circleContainer = createCircleContainer("circle-container");
			var num_of_quastion = createNumOfQuastion(i);
			circleContainer.appendChild(num_of_quastion);

			var letters = ["", "", "", "", ""];
			for (var j = 0; j < letters.length; j++) {
				var circle = createCircle(letters[j]);
				circleContainer.appendChild(circle);
			}

			columnClass.appendChild(circleContainer);

		}
	} else {
		alert("Please enter a value greater than 0");
	}
}

function createIdNum() {
	rowNum = 5
	colNum = 9

	var mainContainer = document.getElementById("num_id_child");

	var p_num_id_child = createCircleContainerp("p_num_id_child");
	mainContainer.appendChild(p_num_id_child);

	function createCircleContainer(className) {
		var circleContainer = document.createElement("div");
		circleContainer.className = className;
		return circleContainer;
	}

	function createCircleContainerp(className) {
		var circleContainerul = document.createElement("p");
		circleContainerul.className = className;
		return circleContainerul;
	}


	function createCircle(num) {
		var circle = document.createElement("div");
		circle.className = "circle";
		var letter = document.createElement("span");
		letter.className = "letter";
		letter.innerHTML = num;
		circle.appendChild(letter);
		return circle;
	}


	for (let i = 0; i <= rowNum; i++) {
		var num_id_child = createCircleContainer("num_id_child");

		for (var j = colNum; j >= 0; j--) {
			var circle = createCircle(j);
			num_id_child.appendChild(circle);
		}

		p_num_id_child.appendChild(num_id_child);

	}
}

window.onload = function() {
	createIdNum();
  };

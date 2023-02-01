function addFaculty(idx, faculties, courses) {
    //     // var arr = [];
    //     // console.log(i)
    //     // console.log(idx)

    // console.log(idx, faculties, courses);
    for (var eachIDX of idx) {
        var div = document.getElementById("course" + eachIDX);
        // for (var i = 0; i < faculties.length; i++) {
        for (var j = 0; j < faculties[eachIDX - 1].length; j++) {
            var checkbox = document.createElement("input");
            var label = document.createElement("label");
            checkbox.type = "checkbox";
            checkbox.id = "checkbox" + eachIDX + j;
            checkbox.name = "checkboxFaculty" + eachIDX;
            checkbox.value = faculties[eachIDX - 1][j];
            // checkbox.checked = true;
            label.innerHTML = faculties[eachIDX - 1][j] + ":";
            label.htmlFor = faculties[eachIDX - 1][j];
            div.appendChild(label);
            div.appendChild(checkbox);
        }
    }
    return faculties
}
// }
async function getFaculties() {
    var no = document.getElementById("no_of_courses").value;
    var courseFaculties = [];
    var idx = [];
    var courses = [];
    for (var i = 1; i <= no; i++) {
        idx.push(i);
        var input = document.getElementById("Course" + i).value;
        courses.push(input);

    }

    // var xhr = new XMLHttpRequest();
    // xhr.open("POST", "/process_input", true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    // xhr.send(JSON.stringify({ courses: courses }));
    // xhr.onload = function () {
    //     var allFaculties = JSON.parse(xhr.responseText);
    //     for (var eachCourseFaculty of allFaculties) {
    //         var uniqueFaculties = new Set(eachCourseFaculty);
    //         var faculties = Array.from(uniqueFaculties);
    //         courseFaculties.push(faculties);
    //     }
    // }

    await axios.post("/process_input", { courses: courses, no: no })
        .then(function (response) {
            var allFaculties = response.data;
            for (var eachCourseFaculty of allFaculties) {
                //     var uniqueFaculties = new Set(eachCourseFaculty);
                //     var faculties = Array.from(uniqueFaculties);
                courseFaculties.push(eachCourseFaculty);
            }

        })
        .catch(function (error) {
            console.log(error);
        });
    // console.log(idx, courseFaculties, courses);
    return [idx, courseFaculties, courses];


}

function coursesNO() {
    var no = document.getElementById("no_of_courses").value;
    document.getElementById("no_of_courses").disabled = true;
    var button = document.createElement("input");
    var field_set = document.createElement("fieldset");
    field_set.id = "allcourses1";
    var legend = document.createElement("legend");
    legend.innerHTML = "Select Courses";
    field_set.appendChild(legend);
    document.getElementById("coursescontainer").appendChild(field_set);

    for (var i = 1; i <= no; i++) {
        var div = document.createElement("div");
        div.name = "courses"
        div.id = "course" + i;
        div.style.padding = "5px";
        var textfield = document.createElement("input");
        var label = document.createElement("label");
        label.innerHTML = "Course " + i + ":  ";
        label.for = "Course" + i;
        textfield.type = "text";
        textfield.value = "";
        textfield.id = "Course" + i;
        textfield.name = "course";

        document.getElementById("allcourses1").appendChild(div);
        document.getElementById("course" + i).appendChild(label);
        document.getElementById("course" + i).appendChild(textfield);

        document.getElementById("allcourses1").appendChild(document.createElement("br"));
        document.getElementById("allcourses1").appendChild(document.createElement("br"));

    }
    document.getElementById("allcourses1").appendChild(button);
    button.type = "button";
    button.value = "Get Faculties";
    var courses = [];
    button.onclick = async function () {
        let [idx, courseFaculties, courses] = await getFaculties();
        // console.log(idx, courseFaculties, courses);
        addFaculty(idx, courseFaculties, courses);
        // disable button
        button.disabled = true;

        // for (var eachIDX of idx) {
        //     // console.log("course" + eachIDX);
        //     for (var i = 0; i < courseFaculties.length; i++) {
        //         // console.log(courseFaculties[i]);
        //         for (var j = 0; j < courseFaculties[i].length; j++) {
        //             var checkbox = document.createElement("input");
        //             var label = document.createElement("label");
        //             checkbox.type = "checkbox";
        //             checkbox.id = "checkbox" + eachIDX + j;
        //             checkbox.name = "checkboxFaculty";
        //             checkbox.value = courseFaculties[i][j];
        //             label.innerHTML = courseFaculties[i][j] + ":";
        //             label.htmlFor = courseFaculties[i][j];
        //             document.getElementById("course" + eachIDX).appendChild(label);
        //             document.getElementById("course" + eachIDX).appendChild(checkbox);
        //         }
        //     }

        // }
    }
}
function getCourses() {
    var no = document.getElementById("no_of_courses").value;
    var courses = [];
    for (var i = 1; i <= no; i++) {
        var course = document.getElementById("Course" + i).value;
        courses.push(course);
    }
    // console.log(courses);
    return courses;
}
// function getFaculties(){

// }
function getDays() {
    var days = [];
    var dayscontainer = document.getElementById("dayscontainer");
    var inputs = dayscontainer.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].checked) {
            days.push(inputs[i].value);
        }
    }
    // console.log(days);
    return days;
}
function getTimes() {
    var times = [];
    var timescontainer = document.getElementById("timescontainer");
    var inputs = timescontainer.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].checked) {
            times.push(inputs[i].value);
        }
    }
    // console.log(times);
    return times;
}
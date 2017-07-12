/**
 * Created by ScottWeitzner on 7/11/17.
 */

function makeErrorToast(message) {
    Materialize.toast(message, 2000, 'red lighten-3')
}

function makeGoodToast(message) {
    Materialize.toast(message, 2000, 'green lighten-3')
}

function createSkillSuggestionTags(suggestions) {
    var tags = [];
    suggestions.forEach(function (s) {
       var tag = {tag: s};
       tags.push(tag);
    });

    $('.skills.chips').material_chip();
    $('.skills.chips-initial').material_chip({
        data: tags
    });
    $('.skills.chips-placeholder').material_chip({
        placeholder: 'Enter a Skill'
     });
}

function createInterestSuggestionTags(suggestions) {
    var tags = [];
    suggestions.forEach(function (s) {
       var tag = {tag: s};
       tags.push(tag);
    });

    console.log(tags)

    $('.interests.chips').material_chip();
    $('.interests.chips-initial').material_chip({
        data: tags
    });
    $('.interests.chips-placeholder').material_chip({
        placeholder: 'Enter an Interest'
     });
}

function addNewSkills() {
    var data = $('.skills.chips').material_chip('data');

    var tags = [];
    data.forEach(function (tag) {
       tags.push(tag['tag']);
    });

    var body = {
        tags : tags
    };

    $.ajax({
        url: '/add_skills',
        data: JSON.stringify(body),
        contentType: 'application/json;charset=UTF-8',
        type: 'POST',
        success: function() {
            location.reload();
        }
    });
}

function addNewInterests() {
    var data = $('.interests.chips').material_chip('data');

    var tags = [];
    data.forEach(function (tag) {
       tags.push(tag['tag']);
    });

    var body = {
        tags : tags
    };

    $.ajax({
        url: '/add_interests',
        data: JSON.stringify(body),
        contentType: 'application/json;charset=UTF-8',
        type: 'POST',
        success: function() {
            location.reload();
        }
    });
}
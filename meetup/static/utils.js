/**
 * Created by Scott Weitzner on 7/11/17.
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

var EventType = {
    GENERAL: 0,
    RECOMMENDED: 1
}


function attendEvent(index, element, event){

    console.log(index)

    if ( event === EventType.GENERAL ){
        console.log('here')
        var current_event = current_available_events[index-1];
    }
    if ( event === EventType.RECOMMENDED){
        console.log('here')
        current_event = recommended_events[index-1];
    }

    console.log(current_event);

    var body = {
        title : current_event['title'],
        date : current_event['date'],
        time : current_event['time']
    };

    makeGoodToast("You've been marked as going!");

    $.ajax({
        url: '/attend_event',
        data: JSON.stringify(body),
        contentType: 'application/json;charset=UTF-8',
        type: 'POST'
    });

    $(element).addClass('disabled')

}

function noLongerAttendEvent(index, element){

    var current_event = events_going_to[index-1];

    var body = {
        title : current_event['title'],
        date : current_event['date'],
        time : current_event['time']
    };

    makeErrorToast("You've been taken off the attendance");

    $.ajax({
        url: '/no_longer_attend_event',
        data: JSON.stringify(body),
        contentType: 'application/json;charset=UTF-8',
        type: 'POST'
    });

    $(element).addClass('disabled')

}
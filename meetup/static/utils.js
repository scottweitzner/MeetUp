/**
 * Created by ScottWeitzner on 7/11/17.
 */

function makeErrorToast(message) {
    Materialize.toast(message, 2000, 'red lighten-3')
}

function makeGoodToast(message) {
    Materialize.toast(message, 2000, 'green lighten-3')
}
// create a js file to capture how we want to display stuff after submission
var TR = function() {
    this.calculateScore = function() {
        var answerVals = this.getAnswersVals();
        var totalAnswers = answerVals.correct + answerVals.wrong;
        var score = answerVals.correct / totalAnswers;
        score = Math.ceil(score * 100);
        return score;
    };
    this.getAnswersVals = function() {
        var answerElms = jQuery('.is-correct');
        var answerVals = {correct: 0, wrong: 0};
        var correct;
        var wrong;
        answerElms.each(function() {
            if (jQuery(this).text() == 'False') {
                answerVals.wrong += 1;
            }
            if (jQuery(this).text() == 'True') {
                answerVals.correct += 1;
            }
        });
        return answerVals;
    };
    this.showFeedback = function(tr) {
        if (this.calculateScore() > 80) {
            this.showPassFeedback();
        } else {
            this.showFailFeedback(tr);
        }

        this.showScore();
    };
    this.showPassFeedback = function() {
        jQuery('#feedback .pass').css({
            display: 'block'
        });
    };
    this.showFailFeedback = function(tr) {
        var weaknessElm = jQuery('#feedback .weakness');
        var weaknesses = this.getSubjectWeakness();
        jQuery(weaknesses).each(function() {
            weaknessElm.append('<div class="subject"><p>' +
                               tr.subjectRef[this] + '</p></div>');
        });
        weaknessElm.css({
            display: 'block'
        });
        jQuery('#feedback .fail').css({
            display: 'block'
        });
    };
    this.getSubjectWeakness = function() {
        var wrongAnswers = jQuery('.is-correct.False');
        var subjectRef = {};
        var subjects = [];
        wrongAnswers.each(function() {
            var s = jQuery(this).parent().children('li.quiz-type').text();
            var ref  = jQuery(this).parent()
                .children('li.quiz-description').text();
            subjectRef[s] = ref;
            subjects.push(s);
        });
        this.subjectRef = subjectRef;
        return jQuery.unique(subjects);
    };
    this.showScore = function() {
        var score = this.calculateScore();
        var pass = 'fail';
        if (score > 79) {
            pass = 'pass';
        }
        jQuery('#score .percentage').addClass(pass).append(score + '%');
    };
};

jQuery(document).ready(function() {
    var tr = new TR();
    tr.showFeedback(tr);
});

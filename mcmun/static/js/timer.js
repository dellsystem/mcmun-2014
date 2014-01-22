(function() {
    var Timer = function() {
        var interval = null;
        var numSeconds = 0;
        var desiredTime = 30;

        var resetClock = function() {
            clearInterval(interval);
            numSeconds = 0;
            $('#timer .clock').removeClass('done');
            $('#timer .clock').text('00:00');
        };

        this.setDesiredTime = function(time) {
            desiredTime = time;
        };

        this.start = function() {
            // Update the button colours
            $('#start-timer').addClass('disabled');
            $('#next-timer').removeClass('disabled');
            $('#stop-timer').removeClass('disabled');

            resetClock();

            var clock = $('#timer .clock');
            var self = this;

            // Update the displayed time on the clock every second
            interval = setInterval(function() {
                numSeconds++;

                var minutes = parseInt(numSeconds / 60);
                var seconds = numSeconds % 60;

                // Add leading 0 if necessary
                if (minutes < 10) {
                    minutes = '0' + minutes;
                }

                if (seconds < 10) {
                    seconds = '0' + seconds;
                }

                clock.text(minutes + ':' + seconds);

                // Once we're done, make it red
                if (numSeconds >= desiredTime) {
                    self.stop();
                }
            }, 1000);
        };

        this.stop = function() {
            // Update the button colours
            $('#start-timer').removeClass('disabled');
            $('#next-timer').addClass('disabled');
            $('#stop-timer').addClass('disabled');

            clearInterval(interval);
            $('#timer .clock').addClass('done');
        };
    };

    $(document).ready(function () {
        var timer = new Timer();

        $('#timer .times').on('click', 'li', function() {
            var timeText = $(this).text();
            var i, numMinutes, numSeconds, desiredTime;

            if ($(this).hasClass('other')) {
                // deal with other times
                // fuck it i don't care
                while (true) {
                    timeText = prompt("Enter desired time (MM:SS)", "00:00");
                    i = timeText.indexOf(':');
                    numMinutes = parseInt(timeText.substring(0, i), 10);
                    numSeconds = parseInt(timeText.substring(i + i), 10);
                    desiredTime = numSeconds + (numMinutes * 60);

                    if (desiredTime > 0) {
                        // Update the li to reflect the set time
                        $(this).text('other (' + timeText + ')');
                        break;
                    } else {
                        timeText = prompt("Invalid time; try again", "00:00");
                    }
                }
            } else {
                i = timeText.indexOf(':');
                numMinutes = parseInt(timeText.substring(0, i), 10);
                numSeconds = parseInt(timeText.substring(i + 1), 10);
                desiredTime = numSeconds + (numMinutes * 60);
            }

            timer.setDesiredTime(desiredTime);
            $('#timer .times .active').removeClass('active');
            $(this).addClass('active');
        });

        var addButtonEvent = function(buttonId, callback) {
            $(buttonId).on('click', function() {
                if (!$(this).hasClass('disabled')) {
                    callback();
                }
            });
        };

        addButtonEvent('#start-timer', function() {
            timer.start();
        });

        addButtonEvent('#next-timer', function() {
            timer.stop();
            timer.start();
        });

        addButtonEvent('#stop-timer', function() {
            timer.stop();
        });
    });
})();

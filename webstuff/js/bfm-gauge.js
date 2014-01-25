/**
 * Created with PyCharm.
 * User: jonc
 * Date: 29/11/2012
 * Time: 19:44
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function() {
    // set defaults for the radial gauge control
    var radialGaugeOptions = $.wijmo.wijradialgauge.prototype.options;

    // override only the settings we want to change for this app
    radialGaugeOptions.cap.radius = 10;
    radialGaugeOptions.cap.style = { fill: '270-#fbb714-#e87d11', stroke: 'none' };
    radialGaugeOptions.pointer.style = { fill: '90-#fbb714-#e87d11', stroke: 'none' };
    radialGaugeOptions.face.style = { fill: 'none', stroke: 'none' };
    radialGaugeOptions.startAngle = 0;
    radialGaugeOptions.sweepAngle = 180;
    radialGaugeOptions.min = 0;
    radialGaugeOptions.max = 300;
    radialGaugeOptions.tickMajor.interval = 50;
    radialGaugeOptions.tickMajor.style = { fill: '#666', stroke: 'none' };
    radialGaugeOptions.tickMinor.interval = 10;
    radialGaugeOptions.tickMinor.style = { fill: '#666', stroke: 'none' };
    radialGaugeOptions.labels.format = function (val) { return Globalize.format(val, 'c0') + 'M' };
    radialGaugeOptions.labels.visible = false;
    radialGaugeOptions.origin = { x: 0.5, y: 0.8 };
    radialGaugeOptions.height = 300;
    radialGaugeOptions.width = 500;
    radialGaugeOptions.radius = 200;
    //radialGaugeOptions.animation = { enabled: false };
    radialGaugeOptions.ranges = [{ startWidth: 22, endWidth: 22, startValue: 0, endValue: 300, startDistance: 0.7, endDistance: 0.7, style: { fill: "0-#0f0-#f00", stroke: "none", opacity: 0.2}}];

    // apply default options to the radial gauge
    $.extend($.wijmo.wijradialgauge.prototype.options, radialGaugeOptions);
});
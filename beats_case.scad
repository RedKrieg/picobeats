use <geodesic_sphere.scad>

unicorn_width = 25;
unicorn_length = 62.5;
unicorn_height = 1.8;
unicorn_button_height = 1.6;
unicorn_edge_to_button = 4.4;
unicorn_edge_to_led = 0.4;
unicorn_led_height = 1.2;
button_length = 4.4;
button_width = 5.2;
pico_width = 21.4;
pico_pin_height = 2.4 ;
header_width = 20.5;
header_length = 51.5;
wall_thickness = 1.6;
package_height = 14.4;
usb_header_length = header_length/2+wall_thickness*2;
usb_header_width = 9;
usb_header_height = 3.8;
usb_header_pico_offset = 1.6;
usb_plug_width = 12;
usb_plug_height = 8.4;
bootsel_width = 3.5;
bootsel_length = 25;
bootsel_height = usb_header_height;
bootsel_pico_width_offset = 12.3;
debug_header_length = usb_header_length;
debug_header_width = 6;
debug_header_height = 3.4;

$fn=12;

module rounded_cube(length, width, height, radius) {
    hull() {
        for (l=[0+radius,length-radius], w=[0+radius,width-radius], h=[0+radius,height-radius]) {
            translate([l, w, h]) geodesic_sphere(radius);
        }
    }
}

module package() {
    translate([wall_thickness, wall_thickness, wall_thickness+usb_header_height-pico_pin_height]) union() {
        //unicorn pcb
        translate([0, 0, package_height-unicorn_led_height-unicorn_height]) cube([unicorn_length, unicorn_width, unicorn_height]);
        //cutout for unicorn components
        translate([0, (unicorn_width-header_width)/2, package_height-unicorn_led_height-unicorn_height*2]) cube([unicorn_length, header_width, unicorn_height]);
        //led window
        translate([unicorn_edge_to_button, unicorn_edge_to_led, package_height-unicorn_led_height]) cube([unicorn_length-unicorn_edge_to_button*2, unicorn_width-unicorn_edge_to_led*2, package_height]);
        //buttons
        for (x=[0,unicorn_length-unicorn_edge_to_button], y=[unicorn_edge_to_button,unicorn_width-unicorn_edge_to_button-button_width]) {
            translate([x, y, package_height-unicorn_led_height]) cube([button_length, button_width, package_height]);
        }
        //headers
        translate([(unicorn_length-header_length)/2, (unicorn_width-header_width)/2, 0]) cube([header_length, header_width, package_height]);
        //pico pcb
        translate([(unicorn_length-header_length)/2, (unicorn_width-pico_width)/2, pico_pin_height-0.4]) cube([header_length, pico_width, unicorn_height]);
        //usb header
        translate([(unicorn_length-header_length)/2-usb_header_pico_offset,(unicorn_width-usb_header_width)/2,pico_pin_height-usb_header_height+0.6]) cube([usb_header_length, usb_header_width, usb_header_height]);
        //usb plug
        translate([-wall_thickness*2, (unicorn_width-usb_plug_width)/2, (usb_plug_height-usb_header_height)/2-pico_pin_height-usb_header_height+0.4]) cube([(unicorn_length-header_length)/2-usb_header_pico_offset+wall_thickness*2, usb_plug_width, usb_plug_height]);
        //bootsel
        translate([(unicorn_length-header_length)/2-usb_header_pico_offset+5, (unicorn_width-pico_width)/2+bootsel_pico_width_offset, pico_pin_height-bootsel_height+0.6]) cube([bootsel_length, bootsel_width, bootsel_height]);
        //debug header for pico H
        translate([unicorn_length - (unicorn_length-header_length)/2 - debug_header_length, (unicorn_width-debug_header_width)/2, pico_pin_height-0.4-debug_header_height]) cube([debug_header_length, debug_header_width, debug_header_height]);
    }
}

difference() {
    rounded_cube(unicorn_length+2*wall_thickness, unicorn_width+2*wall_thickness, package_height+wall_thickness*2, wall_thickness);
    package();
}
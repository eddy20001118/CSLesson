// DUISC IFY PT ARDUINO EXAMPLE 3 - ANALOGUE OUTPUT TO THE MOTOR
// Yuhao Li 2019

//-----------------------------------------------------------------------------

// motor driver pins
#define PIN_DIRA    12
#define PIN_DIRB    13
#define PIN_PWMA    3
#define PIN_PWMB    11
#define PIN_BRAKEA  9
#define PIN_BRAKEB  8
#define SNSA        A0
#define SNSB        A1

// my pins
#define PIN_LDR_L   A2
#define PIN_LDR_R   A3
#define PIN_BUTTON  20
#define PIN_LED     21

// system constants
#define PRINT_MESSAGE  200
#define MOTOR_UPDATE   20
#define LED_BLINK      500
#define LED_BLINK_FAST  50

// default values
#define PWMA_DIR LOW
#define PWMB_DIR HIGH
#define LDR_WINDOW  20
#define LDR_WINDOW_CORNER 50
#define LDR_SUM_WINDOW 150
#define NORMAL_SPEED 70
#define CORNER_SPEED 130
#define MAX_SPEED 255
#define LOOP_TO_STOP 3
//-----------------------------------------------------------------------------

// GLOBAL VARIABLES

// motor controller values
unsigned int g_pwm_A;                     // PWM speed value for motor A
unsigned int g_pwm_B;                     // PWM speed value for motor B
byte g_dir_A;                             // directon A: LOW=anticlockwise; HIGH=clockwise
byte g_dir_B;                             // directon A: LOW=anticlockwise; HIGH=clockwise

// sensor values
unsigned int g_ldr_left;                  // right ldr value
unsigned int g_ldr_right;                 // left ldr value
int g_ldr_diff;                           // ldr difference
int g_ldr_offset;                         // ldr offset
int g_ldr_sum;                            // ldr sum, higher when detecting the while tape
int g_ldr_sum_initial;                    // initial sum of ldr values (black line)

//status of the white tape detecting
bool g_white_tape_entered;                // True: have entered the white tape; False: leave the white tape

// led value
byte g_led;                               // led state
bool g_led_blink_speed;                   // led blink fast or not

// robot working variables
bool g_motor_enabled;                     // enable/disable the motors

// system variables
unsigned long g_loop_counter_serial;      // loop counter for serial port
unsigned long g_loop_motor;               // loop counter for motor update
unsigned long g_loop_led_blink;           // loop counter for led to blink
unsigned long g_white_tape_count;         // counter for the while tape
//-----------------------------------------------------------------------------

// SETUP

void setup()
{
  // set default +5V for analogue reference
  analogReference(DEFAULT);
  
  // set pin modes
  pinMode(PIN_DIRA,OUTPUT);
  pinMode(PIN_DIRB,OUTPUT);
  pinMode(PIN_PWMA,OUTPUT);
  pinMode(PIN_PWMB,OUTPUT);
  pinMode(PIN_BRAKEA,OUTPUT);
  pinMode(PIN_BRAKEB,OUTPUT);
  pinMode(PIN_BUTTON,INPUT_PULLUP);
  pinMode(PIN_LED,OUTPUT);
  
  // disable breaking
  digitalWrite(PIN_BRAKEA,LOW);   // disable brake A
  digitalWrite(PIN_BRAKEB,LOW);   // disable brake B

  // set interrput button, when pressed, switch the status of robot's motors
  attachInterrupt(digitalPinToInterrupt(PIN_BUTTON), standby, FALLING);
  
  // set initial counters
  g_loop_counter_serial = 0;
  g_loop_motor = 0;
  g_loop_led_blink = 0;
  g_white_tape_count = 0;
  
  // set initial values for motor
  g_pwm_A = 0;
  g_pwm_B = 0;
  g_dir_A = PWMA_DIR;
  g_dir_B = PWMB_DIR;
  g_motor_enabled = false;
  g_white_tape_entered = false;   // robot should start at the black line

  // set initial values for led
  g_led = HIGH;
  g_led_blink_speed = false;

  // read and calculate initial ldr values
  g_ldr_left = analogRead(PIN_LDR_L);
  g_ldr_right = analogRead(PIN_LDR_R);
  g_ldr_offset = g_ldr_left - g_ldr_right;
  g_ldr_sum_initial = g_ldr_left + g_ldr_right;

    
  // write led output
  my_write_led_output();
  
  // initialise serial comms port and display startup message
  Serial.begin(9600);
  Serial.println("starting motor driver test...");
  
  delay(2000);
}

//-----------------------------------------------------------------------------

// MAIN LOOP

void loop()
{
  // local variables
  char serial_message[255];
 
  // set the default speed and direction
  g_pwm_A = MAX_SPEED;
  g_pwm_B = MAX_SPEED;
  g_dir_A = PWMA_DIR;
  g_dir_B = PWMB_DIR;
  
  // set the default led value
  g_led = HIGH;
  
  // check MOTOR loop counter and update values
  if (g_loop_motor >= MOTOR_UPDATE)
  {
    // read inputs
    my_read_sensor_inputs();

    // calculate the speed and overwrite it
    my_motor_speed_cal();
    
    // reset the loop counter
    g_loop_motor = 0;

    my_write_motor_outputs();
  }

  // check SERIAL loop counter and print motor value
  if (g_loop_counter_serial >= PRINT_MESSAGE)
  {
    sprintf(serial_message,"motor A = %d,%d; motor B = %d,%d; ldr_offset = %d; ldr_diff = %d; sum = %d; initial_sum = %d tape_count=%d",g_pwm_A,g_dir_A,g_pwm_B,g_dir_B,g_ldr_offset,g_ldr_diff,g_ldr_sum,g_ldr_sum_initial,g_white_tape_count);
    Serial.println(serial_message);

    // reset loop counter
    g_loop_counter_serial = 0;
  }

  // LED blinking while motors are enabled
  // LED remains on when motors are disabled
  if(g_motor_enabled)
  {
    
    // the first half period led will be HIGH as default at begining of loop()
    // the last half period led will be LOW
    if(!g_led_blink_speed)
    {
      if (g_loop_led_blink >= 0.5 * LED_BLINK && g_loop_led_blink <= LED_BLINK)
      {
        g_led = LOW;
      }
      //reset the loop counter 
      else if (g_loop_led_blink >= LED_BLINK)
      {
        g_loop_led_blink = 0;
      }  
    }
    else
    {
      if (g_loop_led_blink >= 0.5 * LED_BLINK_FAST && g_loop_led_blink <= LED_BLINK_FAST)
      {
        g_led = LOW;
      }
      //reset the loop counter 
      else if (g_loop_led_blink >= LED_BLINK_FAST)
      {
        g_loop_led_blink = 0;
      }
    }
  }

      
  // write all outputs
  my_write_led_output();
   
  // increment system loop counters
  g_loop_counter_serial++;
  g_loop_motor++;
  g_loop_led_blink++;
  
  // loop delay
  delay(1);
}

//-----------------------------------------------------------------------------

void my_read_sensor_inputs()
{
  g_ldr_left = analogRead(PIN_LDR_L);
  g_ldr_right = analogRead(PIN_LDR_R);
  g_ldr_diff = g_ldr_left - g_ldr_right - g_ldr_offset;
  g_ldr_sum = g_ldr_left + g_ldr_right;

  // if the sum of ldr readings are higher than initial
  // it means the robot detects the white tape
  // therefore turn the 'g_white_tape_entered' variable to True
  
  if(g_ldr_sum >= g_ldr_sum_initial + LDR_SUM_WINDOW)
  {
    g_white_tape_entered = true;
  }
  
  // if the sum is decreasing, and the 'g_white_tape_entered' variable
  // is True, it means the robot is leaving the white tape
  // plus one to the count variable, and reset the 'g_white_tape_entered'
  if(g_ldr_sum <= g_ldr_sum_initial + LDR_SUM_WINDOW && g_white_tape_entered)
  {
    g_white_tape_count++;
    g_white_tape_entered = false;  
  }

  // stop the motors is meets the goal
  if (g_white_tape_count >= LOOP_TO_STOP)
  {
    g_white_tape_count = 0;
    g_motor_enabled = false;  
  }
}

//-----------------------------------------------------------------------------

void my_motor_speed_cal()
{
  // if the ldr difference is small
  // reduce the speed of wheel (of one side) 
  // to make a small turn
  if(g_ldr_diff <= -LDR_WINDOW && g_ldr_diff >= -LDR_WINDOW_CORNER)
  {
    g_pwm_A = NORMAL_SPEED;
    g_led_blink_speed = false;
  }

  if(g_ldr_diff >= LDR_WINDOW && g_ldr_diff <= LDR_WINDOW_CORNER)
  {
    g_pwm_B = NORMAL_SPEED;
    g_led_blink_speed = false;
  }

  // if meets a corner instead of the straight black line,
  // the ldr difference readings should be larger 
  // the direction of the wheel should be reversed to
  // make a bigger turn
  if(g_ldr_diff <= -LDR_WINDOW_CORNER)
  {
    g_pwm_A = CORNER_SPEED;
    g_dir_A = !PWMA_DIR;    //reverse the direction of motor A
    g_led_blink_speed = true;
  }

  if(g_ldr_diff >= LDR_WINDOW_CORNER)
  {
    g_pwm_B = CORNER_SPEED;
    g_dir_B = !PWMB_DIR;    //reverse the direction of motor B
    g_led_blink_speed = true;
  }

}

//-----------------------------------------------------------------------------

void my_write_led_output()
{
  //write led status
  digitalWrite(PIN_LED,g_led);              
}

void my_write_motor_outputs()
{
    // write motor ouputs
  
  // determine whether robot should enable or not
  if(g_motor_enabled)
  {
    // write outputs to motor
    analogWrite(PIN_PWMA,g_pwm_A);    // speed A
    analogWrite(PIN_PWMB,g_pwm_B);    // speed B
    digitalWrite(PIN_DIRA,g_dir_A);   // direction A
    digitalWrite(PIN_DIRB,g_dir_B);   // direction B
  }
  else
  {
    // write outputs to motor
    g_pwm_A = 0;
    g_pwm_B = 0;
    analogWrite(PIN_PWMA,g_pwm_A);    // speed A
    analogWrite(PIN_PWMB,g_pwm_B);    // speed B
  }  
}
//-----------------------------------------------------------------------------

void standby()
{
  g_motor_enabled = !g_motor_enabled;       //switch the status of the button
}

//-----------------------------------------------------------------------------

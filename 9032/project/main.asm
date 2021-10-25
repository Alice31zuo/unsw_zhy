
;Port input - 1.LED - portC 2.LCD - data portF command portA 3. * emergency for portd
;interrupt - 1.system(car to pass or not) 2.emergency 3. push botton to get the car
;Register to use: 
;		1. constant-led, three: 1. west, 2. emergency 3. east
;		2. constant-symbol, 1. < 2.= 3.>
;       3. variable- car 1. the number of car in west, 2. the number of car in east 3. the number of car in road
;						 4. direction  5.time
;push botton for vechicle
;formula: 1. when the cars begin to pass, 0-0.5min no change in the road, 0.5-2.5 the number of cars in the road increase, 2.5-no car in the road, stable or decrease
;		  2. the direction change  at most 5 mins
;		  3. the number of cars update for 0.5mins 
;Port: LED, portc, push botton portD, keypad, portF, LCD, portF
;z5196480
;huiyao zuo 

;constant

.include "m2560def.inc"
.def last = r9           ;control the keypad
.def westled = r10		 ;west turn green
.def roadled = r11		 ;road turn green
.def eastled = r12       ;east turn green
.def direction = r13	 ;0-east,1-west
.def store = r14		 ;store the number
.def exceptlast=r15		 ;0b00011110

.def temp = r16				
.def temp2 = r17
.def westvechile = r18	 ;the number of cars in west
.def eastvechile = r19	 ;the number of cars in east
.def carinroad = r20     ;0b00011111  use bit 1 to show car in the road 
.def flag=r21			 ;control the push botton
.def pair=r22			 ;control the push botton
.def control=r23		 ;signal to the emergency and time count


;Time
.macro Clear             ;use clear to celar the data in the target address
	ldi YL,low(@0)       
	ldi YH,high(@0)
	clr temp
	st Y+, temp
	st Y, temp
.endmacro

;LCD
.macro do_lcd_command    ;use do_lcd_command to send command to lcd 
	ldi r16, @0
	rcall lcd_command
	rcall lcd_wait
.endmacro

;LCD
.macro do_lcd_data       ;use do_lcd_data to send data in register to lcd 
	mov r16, @0
	rcall lcd_data
	rcall lcd_wait
.endmacro

;LCD 
.macro do_lcd_data_cons    ;use do_lcd_data_cons to send data directly to lcd 
	ldi r16, @0
	rcall lcd_data
	rcall lcd_wait 
.endmacro

;LCD
.macro do_lcd_data_num     ;do_lcd_data_num is the marco to transfer the num to ascii
	mov store,@0
	ldi temp2,0
ten:                       ;by substract the 10 to get the ten digit num 
	ldi temp,10
	cp store,temp
	brlo prepare_one
	inc temp2
	sub store,temp
	rjmp ten
prepare_one:               ;to deal with the situation the num do not have tem digit and output the ten gidit num
	cpi temp2,0
	breq one
	ldi temp,$30
	add temp2,temp
	do_lcd_data temp2
	ldi temp2,0
one:                      ;by substract the 1 to get the ten digit num  
	ldi temp,1
	cp store,temp
	brlo prepare_last
	inc temp2
	sub store,temp
	rjmp one
prepare_last:             ;output the last digit num
	ldi temp,$30
	add temp2,temp
	do_lcd_data temp2
	rjmp end
end:
.endmacro

;Time counter
.dseg
SecondCounter: .byte 2    ;set two byte for SecondCounter
TempCounter: .byte 2      ;set two byte for TempCounter

;Interrupt
.cseg
.org 0x0000
	jmp Reset
.org INT0addr            
	jmp EXT_INT0
.org INT1addr
	jmp EXT_INT1
.org OVF0addr
	jmp Timer0OVF


Reset:
	ldi temp,0b00011110       ;use exceptlast to record the followed cars infromation
	mov exceptlast,temp       
	ldi temp,0b11000000       ;use westled to ouput led in the west side
	mov westled, temp
	ldi temp,0b00011000       ;use roadled to ouput led in the emergency
	mov roadled, temp
	ldi temp, 0b00000011      ;use eastled to ouput led in the west side
	mov eastled, temp
	
	clr westvechile           ; clear all the carnum and roadnum
	clr eastvechile
	clr carinroad
	clr last                  ;last is use to 
	clr direction             ;inisial direction is 0 which is east
	ldi control,1             ;control is use to decided wheather there is a emergency
	ldi flag,1                ;use flag to prolong the push button time so that the car num would not increse too quickly
	clr pair                  ;use pair to prolong the push button time so that the car num would not increse too quickly
	clr store                 ;store is a midddle record register 
	
	;led
	ser temp                  ;use portc to output led pattern
	out DDRC,temp

	;keypad
	ldi temp, 0b11110000      
	out DDRF,temp             ;use port F as port of keypad
	ldi temp,0b11101111
	out	PORTF, temp           
	
	;lcd
	ldi r16, low(RAMEND)      ;inicial the value of sp
	out SPL, r16
	ldi r16, high(RAMEND)
	out SPH, r16
	
	;Interrupt 
	ldi temp, (2<<ISC00)|(2<<ISC10)    ;set two interupt as rising egde to triger
	sts EICRA,temp

	in temp, EIMSK
	ori temp, (1<<INT0)|(1<<INT1)      ;enable two interupt
	out EIMSK, temp

	jmp main

;Interrupt west
EXT_INT0:                              ;use pb0 to increase the westvechile
	ldi pair,0                        
	cpi flag,1
	brne TT
	inc westvechile
	ldi flag,0
TT:
	reti

;Interrupt east	
EXT_INT1:                              ;use pb1 to increase the westvechile
	ldi pair,0
	cpi flag,1
	brne YY
	inc eastvechile
	ldi flag,0
YY:
	reti

;Time 0.5s
Timer0OVF:                             ;timer 0.5s refresh one time
	push temp
	push YH
	push YL
	push r25
	push r24
	ldi YL,low(TempCounter)
	ldi YH, high(TempCounter)
	ld r24, Y+
	ld r25, Y
	adiw r25:r24,1

	cpi r24, low(500)                  ;count 500*64*256/16MHZ ~= 0.5
	brne NotSecond
	cpi r25, high(500)
	brne NotSecond

	rjmp LCD
Next:
	clr temp2
	
	Clear TempCounter
	ldi YL, low(SecondCounter)
	ldi YH, high(SecondCounter)
	ld r24, Y+
	ld r25, Y
	adiw r25:r24,1
	st Y,r25
	st -Y,r24
	rjmp endif

NotSecond:
	inc pair    ;use pair to deal with debouncing
	st Y, r25
	st -Y, r24
	cpi pair,150    ;when pair=150 ,then set flag to 1 ,means the push can count
	brsh update
	rjmp endif
update:
	ldi flag,1      ;flag =1
	rjmp endif

endif:
	;read the key pad
	in	temp2, PINF            ;read the keypad
	andi temp2,0x0F
	cpi temp2, 0b00000111       
	breq controlset
	rjmp Nextto
controlset:                    ;when '*' is push 
	cp temp2,last              ;temp2 and last is not equal mean the 
	breq Nextto

	inc control                ;change the control between 0 and 1 ,when control ==0 ,means emmergency
	ldi temp,0b00000001
	and control,temp
	rjmp Nextto

Nextto:
	mov last,temp2            ;record the last situation of keypad
	pop r24
	pop r25
	pop YL
	pop YH
	pop temp
	reti

LCD:
	ser r16
	out DDRF, r16            ;when in lcd ,use port f and port a send data and command to lcd
	out DDRA, r16
	clr r16
	out PORTF, r16
	out PORTA, r16

	do_lcd_command 0b00111000 ; 2x5x7
	rcall sleep_5ms
	do_lcd_command 0b00111000 ; 2x5x7
	rcall sleep_1ms
	do_lcd_command 0b00111000 ; 2x5x7
	do_lcd_command 0b00111000 ; 2x5x7
	do_lcd_command 0b00001000 ; display off
	do_lcd_command 0b00000001 ; clear display
	do_lcd_command 0b00000110 ; increment, no display shift
	do_lcd_command 0b00001110 ; Cursor on, bar, no blink

LCD_print:                         ;print the car number in west
	do_lcd_data_num westvechile 
	ldi temp,1
	cp direction,temp
	breq Print_west
Print_east:                         ;print the direction 
	do_lcd_data_cons '<'
	do_lcd_data_cons '<'
	ldi temp2,0
	mov store,carinroad
	rjmp print_equal
Print_west:                         ;print the direction 
	do_lcd_data_cons '>'
	do_lcd_data_cons '>'
	ldi temp2,0
	mov store,carinroad
print_equal:                        ;print the car in road
	cpi temp2,5
	breq east
	inc temp2
	ldi temp,0b00011110
	mov exceptlast,temp               
	and exceptlast,carinroad           ;when last num is 1 ,it would output =
	andi carinroad,0b00000001
	cpi carinroad,0b00000001
	breq print_cons
	mov carinroad,exceptlast
	lsr carinroad
	rjmp print_equal
print_cons:                        ;if last is 1 ,print '='
	do_lcd_data_cons '='
	mov carinroad,exceptlast       
	lsr carinroad                  ;lsr the carinroad to print next car or gap
	rjmp print_equal
east:
	mov carinroad,store            ;recover the carinroad
	do_lcd_data_num eastvechile    ;print the car num of east
	ldi temp,0b00011110
	mov exceptlast,temp	 
	rjmp Number_update

Number_update:
	ldi temp, 0b11110000      ;because the lcd and keypad all link to port f ,so this port f need set to read the keypad 
	out DDRF,temp
	ldi temp,0b11101111
	out	PORTF, temp
	cpi control,0             ;when control is 0 ,means there is a emmergency situation
	breq Middle               ;use a middle to solve the problem breq cannot jump to emerency directly
Nexttt:
	ldi temp,0                ;get the current direction 
	cp direction,temp         
	breq east_update
	brne west_update

east_update:                  ;one side update ,the other side 's logic is same 
	cpi control,11            ;when other side have car , it need to consider the congestion situation . and 5mins would have 10 car to run
	breq wait_east            ;this means the side have already to pass 10 cars 
	out PORTC, eastled        ;output the led light pattern
	lsr carinroad             ;refresh the carinroad

	cpi eastvechile,0         ;know the catr in this side to decide it can sub 1 or not
	breq compare_carroade

	dec eastvechile           ;decrease the car
	ldi temp,0b00010000       ;a new car into the road
	or carinroad,temp       

	cpi westvechile,0         ;know the car in otherside to know wheather there need a congestion consideration
	breq UU

	inc control
	rjmp Next
UU:
	ldi control,1
	rjmp Next
compare_carroade:             ; when this have no car and road have no car ,the direction should be change
	ldi control,1
	cpi carinroad,0
	breq change_direction_east   ;change the direction
	rjmp Next

Middle:
	rjmp emergy	

wait_east:                     ;this is congestion situation and east side has already have pass 5mins cars
	ldi temp,0b00000000        ;so the led output the 0 pattern ,because no side can in cars
	out PORTC, temp
	lsr carinroad              ;let car in road pass
	cpi carinroad,0
	breq change_direction      ;when cars have passed ,change direciton
	rjmp Next

change_direction_east:        ;when the other side have car ,so need to change direciton
	cpi westvechile,0
	brne change_direction
	rjmp Next

west_update:                   ;the other side is mirror as east
	cpi control,11             ;when other side have car , it need to consider the congestion situation . and 5mins would have 10 car to run
	breq wait_west             ;this means the side have already to pass 10 cars 
	out PORTC, westled         ;output the led light pattern
	lsr carinroad              ;update the car in road
	cpi westvechile,0          ;know the car in this side to decide it can sub 1 or not
	breq compare_carroadw      
	dec westvechile            ;decrease the car
	ldi temp,0b00010000        ;add a new cat in road
	or carinroad,temp          
	cpi eastvechile,0          ;when other side have car,need consider the congestion situation
	breq QQ
	inc control
	rjmp Next
QQ:
	rjmp Next
compare_carroadw:              ;when road have no car and other side have no car dont need change direction
	ldi control,1
	cpi carinroad,0
	breq change_direction_west
	rjmp Next

change_direction_west:        ;other side have no car ,change direction
	cpi eastvechile,0
	brne change_direction
	rjmp Next

wait_west:                    ;before change direction ,need wait all the car gone
	ldi temp,0b00000000
	out PORTC, temp
	lsr carinroad
	cpi carinroad,0
	breq change_direction
	rjmp Next

change_direction:                ;change direciton ,change between 0,1
	ldi control,1
	inc direction
	ldi temp,0b00000001
	and direction,temp
	rjmp Next



emergy:                           ;emergency
	ldi temp,0
	ldi temp2,0
Wa:                               ;flash the led
	inc temp
	cpi temp,4
	breq movv
	ldi temp2,0
	out PORTC,temp2
loopP:
	inc temp2
	rcall sleep_5ms
	cpi temp2,20
	brne loopP

	ldi temp2,0
Flash:
	inc temp2
	out PORTC,roadled
	rcall sleep_5ms
	cpi temp2,20
	breq Wa
	rjmp Flash
Movv:                           ;cahnge the car in road is enough ,do not need change car number in each side
	lsr carinroad
	rjmp Next

main:
	;initial 
	out PORTC, eastled         ;initial direciton 
	ldi flag,1                 ;initial can get push
	
	;Time counter
	Clear TempCounter
	Clear SecondCounter
	ldi temp, 0b00000000       ;timer counter set
	out TCCR0A,temp
	ldi temp, 0b00000011       ;presclar value = 64
	out TCCR0B, temp
	ldi temp, 1<<TOIE0          ;enable clock
	sts TIMSK0,temp
	sei                         ;enable global interupt


loop:
	rjmp loop

;For LCD

.equ LCD_RS = 7
.equ LCD_E = 6
.equ LCD_RW = 5
.equ LCD_BE = 4

.macro lcd_set
	sbi PORTA, @0
.endmacro
.macro lcd_clr
	cbi PORTA, @0
.endmacro

;
; Send a command to the LCD (r16)
;

lcd_command:
	out PORTF, r16
	nop
	lcd_set LCD_E
	nop
	nop
	nop
	lcd_clr LCD_E
	nop
	nop
	nop
	ret

lcd_data:
	out PORTF, r16
	lcd_set LCD_RS
	nop
	nop
	nop
	lcd_set LCD_E
	nop
	nop
	nop
	lcd_clr LCD_E
	nop
	nop
	nop
	lcd_clr LCD_RS
	ret

lcd_wait:
	push r16
	clr r16
	out DDRF, r16
	out PORTF, r16
	lcd_set LCD_RW
lcd_wait_loop:
	nop
	lcd_set LCD_E
	nop
	nop
    nop
	in r16, PINF
	lcd_clr LCD_E
	sbrc r16, 7
	rjmp lcd_wait_loop
	lcd_clr LCD_RW
	ser r16
	out DDRF, r16
	pop r16
	ret

.equ F_CPU = 16000000
.equ DELAY_1MS = F_CPU / 4 / 1000 - 4
; 4 cycles per iteration - setup/call-return overhead

sleep_1ms:
	push r24
	push r25
	ldi r25, high(DELAY_1MS)
	ldi r24, low(DELAY_1MS)
delayloop_1ms:
	sbiw r25:r24, 1
	brne delayloop_1ms
	pop r25
	pop r24
	ret

sleep_5ms:
	rcall sleep_1ms
	rcall sleep_1ms
	rcall sleep_1ms
	rcall sleep_1ms
	rcall sleep_1ms
	ret

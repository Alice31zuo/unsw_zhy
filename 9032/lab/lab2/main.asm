;task 3
;a , b ,c = x ,y z
;for n in a,b,c :
; if button : out = n stop
; else : out = n
;

.include "m2560def.inc"

.equ loop_count = 65535
.def iH = r25
.def iL = r24
.def countH = r18
.def countL = r16
.def innerH = r20
.def innerL = r19

first : 
	 rjmp main

delay :                   ;delay
	 cbi DDRF, 2
	 ldi countL, low(loop_count) 
	 ldi countH, high(loop_count)
	 ldi innerL, low(8)
	 ldi innerH, high(8) 
	 clr iH
	 clr iL
	 loopout:             ;two loop
		  clr r27
		  clr r26
		  sbis PINF, 2     ;if push jump
		  rjmp judge
		  cp iL, countL 
		  cpc iH, countH 
		  breq looplight
		  adiw iH:iL, 1
		  Looptwo:
				sbis PINF, 2   ;if push jump
				rjmp judge
				cp r26, innerL
				cpc r27, innerH
				breq loopout
				adiw r27:r26, 1
				nop
				nop
				rjmp Looptwo
judge:                  ;if keep hold
	sbis PINF, 2
	rjmp judge
	rjmp judge2
	 
judge2:                 ; if not hold ,then stop
	sbic PINF, 2
	rjmp judge2
	rjmp judge3

judge3:                ;if push again , jump to looplight
	sbis PINF, 2
	rjmp judge3
	rjmp looplight

main:
	 ldi r16,0b11100000
	 ldi r17,0b11111100
	 ldi r18,0b11111111
	 mov r10, r16
	 mov r11, r17
	 mov r12, r18
	 ldi r16 , 0 
	 ser r17
	 out DDRC, r17      ;use as output
	 out PORTC, r17
	 clr r17
	 out PORTC, r17
	 clr r18
	 out DDRF, r18      ;use as input
	 ser r18
	 out PORTF, r18
	 ldi r22 , 0
	 rjmp looplight
end:
	 rjmp end

looplight:                ;the loop of the light
	 cpi r22 , 0
	 BREQ lp1             ;when 0 p1
	 BRlt lp2             ;when -1 p2
	 brge lp3             ;when 1 p3

lp1:
	 SUBI r22 , 1         ;change the value of r22
	 out PORTC, r10       ;output
	 rjmp delay           ;delay
lp2:
	 SUBI r22 , -2
	 out PORTC, r11
	 rjmp delay
lp3:
	 SUBI r22 , 1
	 out PORTC, r12
	 rjmp delay

version=2
rule=: %timestamp:date-rfc3339% %hostname:word% %tag:word% %message:rest%
rule=: %timestamp:date-rfc3339% %hostname:word% %tag:word%[%pid:number%]: %message:rest%


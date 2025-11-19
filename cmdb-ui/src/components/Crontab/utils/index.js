/* eslint-disable */
/*
    Cron expression validation
    Cron expression format: second, minute, hour, day, month, week, year
    Validation method: returns error message if invalid, returns true if valid
*/
export function cronValidate(cronExpression ){
  // For returning error message
  var message = '';
  // First split the cron expression
  var cronParams = cronExpression.split(" ");
  // Check if cron expression has the correct length, 6 without year, 7 with year, other cases are errors
  if (cronParams.length < 6 || cronParams.length > 7) {
      return "Cron expression requires 6-7 parameters, please re-enter";
  }else{
    // Day and week must have one as ?, or both as *
    if((cronParams[3] == "?" && cronParams[5] != "?") || (cronParams[5] == "?" && cronParams[3] != "?") || (cronParams[3] == "*" && cronParams[5] == "*")){
      // Check if the first position (seconds) is correct
      message = checkSecondsField(cronParams[0]);
      if (message != true) {
          return message;
      }

      // Check if the second position (minutes) is correct
      message = checkMinutesField(cronParams[1]);
      if (message != true) {
          return message;
      }

      // Check if the third position (hours) is correct
      message = checkHoursField(cronParams[2]);
      if (message != true) {
          return message;
      }

      // Check if the fourth position (day) is correct
      message = checkDayOfMonthField(cronParams[3]);
      if (message != true) {
          return message;
      }

      // Check if the fifth position (month) is correct
      message = checkMonthsField(cronParams[4]);
      if (message != true) {
          return message;
      }

      // Check if the 6th position (week) is correct
      message = checkDayOfWeekField(cronParams[5]);
      if (message != true) {
          return message;
      }

      // Check if the seventh position (year) is correct
      if(cronParams.length>6){
        message = checkYearField(cronParams[6]);
        if (message != true) {
            return message;
        }
      }


      return true;
    }else{
      return "When specifying day, week must be set to unspecified (?), when specifying week, day must be set to unspecified (?)"
    }
  }
}
 let message = ''
// Function to check seconds
function checkSecondsField(secondsField) {
  return checkField(secondsField, 0, 59, "second");
}

// Function to check minutes
function checkMinutesField(minutesField) {
  return checkField(minutesField, 0, 59, "minute");
}

// Function to check hours
function checkHoursField(hoursField) {
  return checkField(hoursField, 0, 23, "hour");
}

// Function to check day of month
function checkDayOfMonthField(dayOfMonthField) {
  if (dayOfMonthField == "?") {
      return true;
  }
  if (dayOfMonthField.indexOf("L") >= 0) {
      return checkFieldWithLetter(dayOfMonthField, "L", 1, 7, "day");
  } else if ( dayOfMonthField.indexOf("W") >= 0) {
      return checkFieldWithLetter(dayOfMonthField, "W", 1, 31, "day");
  } else if (dayOfMonthField.indexOf("C") >= 0) {
      return checkFieldWithLetter(dayOfMonthField, "C", 1, 31, "day");
  }
  return checkField( dayOfMonthField, 1, 31, "day");
}

// Function to check month
function checkMonthsField(monthsField) {
  // Handle month abbreviations
  if(monthsField != "*"){
    monthsField=monthsField.replace("JAN", "1");
    monthsField=monthsField.replace("FEB", "2");
    monthsField=monthsField.replace("MAR", "3");
    monthsField=monthsField.replace("APR", "4");
    monthsField=monthsField.replace("MAY", "5");
    monthsField=monthsField.replace("JUN", "6");
    monthsField=monthsField.replace("JUL", "7");
    monthsField=monthsField.replace("AUG", "8");
    monthsField=monthsField.replace("SEP", "9");
    monthsField=monthsField.replace("OCT", "10");
    monthsField=monthsField.replace("NOV", "11");
    monthsField=monthsField.replace("DEC", "12");
    return checkField(monthsField, 1, 12, "month");
  }else{
    return true;
  }

}

// Week validation
function checkDayOfWeekField(dayOfWeekField) {
  dayOfWeekField=dayOfWeekField.replace("SUN", "1" );
  dayOfWeekField=dayOfWeekField.replace("MON", "2" );
  dayOfWeekField=dayOfWeekField.replace("TUE", "3" );
  dayOfWeekField=dayOfWeekField.replace("WED", "4" );
  dayOfWeekField=dayOfWeekField.replace("THU", "5" );
  dayOfWeekField=dayOfWeekField.replace("FRI", "6" );
  dayOfWeekField=dayOfWeekField.replace("SAT", "7" );
  if (dayOfWeekField == "?") {
    return true;
  }
  if (dayOfWeekField.indexOf("L") >= 0) {
      return checkFieldWithLetterWeek(dayOfWeekField, "L", 1, 7, "week");
  } else if (dayOfWeekField.indexOf("C") >= 0) {
      return checkFieldWithLetterWeek(dayOfWeekField, "C", 1, 7, "week");
  } else if (dayOfWeekField.indexOf("#") >= 0) {
      return checkFieldWithLetterWeek(dayOfWeekField, "#", 1, 7, "week");
  } else {
      return checkField(dayOfWeekField, 1, 7, "week");
  }
}

// Function to check year
function checkYearField(yearField) {
  return checkField(yearField, 1970, 2099, "year");
}

// General method to check value range ( - , / *)
function checkField(value, minimal, maximal, attribute) {
  // Check if value contains "-", if so, index will be > 0
  if (value.indexOf("-") > -1 ) {
    return checkRangeAndCycle(value, minimal, maximal,attribute);
  }
  // Check if value contains ",", if so, index will be > 0
  else if (value.indexOf(",") > -1) {
    return checkListField(value, minimal, maximal,attribute);
  }
  // Check if value contains "/", if so, index will be > 0
  else if (value.indexOf( "/" ) > -1) {
    return checkIncrementField( value, minimal, maximal ,attribute);
  }
  // Check if value is "*"
  else if (value=="*") {
    return true;
  }
  // Check individual numbers, letters, and various special characters, etc...
  else {
    return checkIntValue(value, minimal, maximal,true, attribute);
  }
}


// Check if it's an integer and within range, parameters: value to check, lower limit, upper limit, whether to check endpoints, attribute being checked
function checkIntValue(value, minimal, maximal, checkExtremity,attribute) {
  try {
      // Use base 10 to convert to integer
      var val = parseInt(value, 10);
      if (value == val) {
          if (checkExtremity) {
              if (val < minimal || val > maximal) {
                  return (attribute+" parameter value range must be between "+ minimal + "-" + maximal);
              }
              return true;
          }
          return true;
      }
      return (attribute+" parameter contains illegal characters, must be integer or allowed uppercase letters");
  } catch (e) {
      return (attribute+" parameter contains illegal characters, must be an integer~")
  }
}
// Validate if enumeration type parameters are correct
function checkListField(value, minimal, maximal,attribute) {
  var st = value.split(",");
  var values = new Array(st.length);
  // Count the number of times each enumerated number appears in the array, appearing once means no duplication.
  var count=0;
  for(var j = 0; j < st.length; j++) {
      values[j] = st[j];
  }
  // Check if enumeration values are duplicated
  for(var i=0;i<values.length;i++){
    // Check if enumeration values are within range
    message = checkIntValue(values[i], minimal, maximal, true, attribute);
    if (message!=true) {
      return message;
    }
    count=0;
    for(var j=0;j<values.length;j++){
      if(values[i]==values[j])
      {
        count++;
      }
      if(count>1){
        return (attribute+" has duplicate parameters");
      }
    }
  }
  var previousValue = -1;
  // Check if enumeration values are sorted correctly
  for (var i= 0; i < values.length; i++) {
      var currentValue = values[i];
      try {
          var val = parseInt(currentValue, 10);
          if (val < previousValue) {
              return (attribute+" parameters should be sorted from small to large");
          } else {
              previousValue = val;
          }
      } catch (e) {
        // Already validated above, this code is unreachable
        return ("This message is not needed")
      }
  }
  return true;
}

// Validate increment/cycle
function checkIncrementField(value, minimal, maximal, attribute) {
  if(value.split("/").length>2){
    return (attribute + " can only have one '/'");
  }
  var start = value.substring(0, value.indexOf("/"));
  var increment = value.substring(value.indexOf("/") + 1);
  if (start != "*") {
    // Validate if the first value is correct
    message = checkIntValue(start, minimal, maximal, true, attribute);
    if(message != true){
      return message;
    }
    // Validate if the second value is correct
    message = checkIntValue(increment, minimal, maximal, true, attribute);
    if(message != true){
      return message;
    }
    return true;
  } else {
    // Validate if the second value is correct
    return checkIntValue(increment, minimal, maximal, false, attribute);
  }
}

// Validate range
function checkRangeAndCycle(params, minimal, maximal, attribute){
  // Validate that there is only one "-" symbol
  if(params.split("-").length>2){
    return (attribute + " can only have one '-'");
  }
  var value = null;
  var cycle = null;
  // Check if there is a nested cycle within the range
  if(params.indexOf("/") > -1){
    // Validate that there is only one "/" symbol
    if(params.split("/").length>2){
      return (attribute + " can only have one '/'");
    }
    value = params.split("/")[0];
    cycle = params.split("/")[1];
    // Check if the cycle parameter is correct
    message =checkIntValue(cycle, minimal, maximal, true, attribute);
    if (message!=true) {
      return message;
    }
  }else{
    value = params;
  }
  var startValue = value.substring(0, value.indexOf( "-" ));
  var endValue = value.substring(value.indexOf( "-" ) + 1);
  // Check if the first value of the parameter range is correct
  message =checkIntValue(startValue, minimal, maximal, true, attribute);
  if (message!=true) {
    return message;
  }
  // Check if the second value of the parameter range is correct
  message =checkIntValue(endValue, minimal, maximal, true, attribute);
  if(message!=true){
    return message;
  }
  // Check if the start value of the parameter range is less than the end value
  try {
    var startVal = parseInt(startValue, 10);
    var endVal = parseInt(endValue, 10);
    if(endVal < startVal){
      return (attribute+" value range error, start value must be less than end value");
    }
    if((endVal-startVal)<parseInt(cycle,10)){
      return (attribute+" cycle within the value range is meaningless");
    }
    return true;
  } catch (e) {
    // This code is unreachable
    return (attribute+" parameter contains illegal characters, must be an integer");
  }
}

// Check special characters in day field
function checkFieldWithLetter(value, letter, minimalBefore, maximalBefore,attribute) {
  // Check if there is only one letter
  for(var i=0;i<value.length;i++){
    var count = 0;
    if(value.charAt(i)==letter){
      count++;
    }
    if(count>1){
      return (attribute+" value can only have one "+letter+" letter")
    }
  }
  // Validate L
  if(letter == "L"){
    if(value == "LW"){
      return true;
    }
    if(value=="L"){
      return true;
    }
    if(value.endsWith("LW")&&value.length>2)
    {
      return (attribute + " parameter, LW at the end cannot have any letter parameters before it")
    }
    if(!value.endsWith("L"))
    {
      return (attribute + " parameter, L letter cannot have any characters or numbers other than W after it")
    }else{
      var num = value.substring(0,value.indexOf(letter));
      return checkIntValue(num, minimalBefore, maximalBefore, true, attribute);
    }
  }

  // Validate W
  if(letter == "W"){
    if(!value.endsWith("W")){
      return (attribute + " parameter's W must be at the end")
    }else{
      if(value=="W"){
        return (attribute + " parameter's W must have a number before it")
      }
      var num = value.substring(0,value.indexOf(letter));
      return checkIntValue(num, minimalBefore, maximalBefore, true, attribute);
    }
  }

  if(letter == "C"){
    if(!value.endsWith("C")){
      return (attribute + " parameter's C must be at the end")
    }else{
      if(value=="C"){
        return (attribute + " parameter's C must have a number before it")
      }
      var num = value.substring(0,value.indexOf(letter));
      return checkIntValue(num, minimalBefore, maximalBefore, true, attribute);
    }
  }
}

// Check special characters in week field
function checkFieldWithLetterWeek(value, letter, minimalBefore, maximalBefore,attribute) {
  // Check if there is only one letter
  for(var i=0;i<value.length;i++){
    var count = 0;
    if(value.charAt(i)==letter){
      count++;
    }
    if(count>1){
      return (attribute+" value can only have one "+letter+" letter")
    }
  }
  // Validate L
  if(letter == "L"){
    if(value=="L"){
      return true;
    }
    if(!value.endsWith("L"))
    {
      return (attribute + " parameter, L letter must be the last position")
    }else{
      var num = value.substring(0,value.indexOf(letter));
      return checkIntValue(num, minimalBefore, maximalBefore, true, attribute);
    }
  }

  if(letter == "C"){
    if(!value.endsWith("C")){
      return (attribute + " parameter's C must be at the end")
    }else{
      if(value=="C"){
        return (attribute + " parameter's C must have a number before it")
      }
      var num = value.substring(0,value.indexOf(letter));
      return checkIntValue(num, minimalBefore, maximalBefore, true, attribute);
    }
  }

  if(letter == "#"){
    if(value=="#"){
      return (attribute + " # must have integers before and after");
    }
    if(value.charAt(0)==letter){
      return (attribute + " # must have an integer before it")
    }
    if(value.endsWith("#")){
      return (attribute + " # must have an integer after it")
    }
    var num1 = value.substring(0,value.indexOf(letter));
    var num2 = value.substring(value.indexOf(letter)+1,value.length)
    message = checkIntValue(num1, 1, 4, true, (attribute+" before #"));
    if(message!=true){
      return message;
    }
    message = checkIntValue(num2, minimalBefore, maximalBefore, true, (attribute+" after #"));
    if(message!=true){
      return message;
    }
    return true;
  }
}
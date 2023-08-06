To build a robust application, it takes a lot of effort to properly check and validate everything that can goes wrong within an input file filled by users:
 - Wrong option name : login VS username,
 - Wrong type : string instead of integer,
 - Mandatory information missing
 - Value not conform (ip address not valid etc ..)

All this complexity is often not completely managed by the application has it require a LOT of work: Defconf is here to help, it will:
 - Validate the format of the configuration file (list, dict, string)
 - Validate all names and track unsupported options
 - Validate content type (integer, string, bool, list, dict)
 - Validate the value with REGEX or pre-define list
 - Populate default value if information is missing

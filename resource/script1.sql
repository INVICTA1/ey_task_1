DROP schema if exists `ey`;
CREATE SCHEMA IF NOT EXISTS `ey` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `ey`;


CREATE TABLE `random_data` (
  `date` DATE NOT NULL ,
  `english_sequence` VARCHAR(45) NOT NULL,
  `russian_sequence` VARCHAR(45) NOT NULL,
  `digit_sequence` INT NOT NULL,
  `decimal_sequence` float NOT NULL,
   index  `digit_sequence_idx` (`digit_sequence` asc));

 DELIMITER |

create procedure sum_int_and_average_median()
begin
declare sum_int,average_median double;
set sum_int = (select sum(digit_sequence) from random_data);
set average_median= (select decimal_sequence from(select  row_number() over(order by decimal_sequence ) as number_row,decimal_sequence from random_data   ) as row_table
where (select floor(count(*)/2) from random_data) = number_row);
select sum_int,average_median;
end
|


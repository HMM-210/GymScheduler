package main

//importing packages
import (
	//"encoding/json"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"
	"runtime"
	"image"
	"image/color"
	"image/draw"
	"golang.org/x/image/font"
	"github.com/01walid/goarabic"
	"golang.org/x/image/math/fixed"
	"golang.org/x/image/font/opentype"
	"image/png"
	
	
)

// important variables
var file_name string = "requests.json"
var main_path string = GetGolangFilePath()
var image_path string 
type TextPosition struct {
    X int
    Y int
}


// functions in function
func GetGolangFilePath() string {
	_, filename, _, ok := runtime.Caller(0)
    	if !ok {
    	    return ""
		}
		return filepath.Dir(filename)
}

func GetEXEFilePath() string {
    ex, err := os.Executable()
    if err != nil {
        return ""
    }
    return filepath.Dir(ex)
}

func is_file_exist(file_name string) bool {
	json_file_path := filepath.Join(main_path, file_name)
	_, err := os.Stat(json_file_path)


	if errors.Is(err, os.ErrNotExist) {
		return false
	} else if err != nil {
		return false
	} else {
		return true
	}
}

func read_file(file_name string) (map[string]interface{}, bool) {
	var reading_file []byte
	var err error

	reading_file,  err = os.ReadFile(file_name)
	if err != nil {
		fmt.Println("السبب للخطأ هو:", err)
		return nil, false
	}
	var data map[string]interface{}
	err = json.Unmarshal(reading_file, &data)
	if err != nil {
		fmt.Println("السبب للخطأ هو:", err)
		return nil, false
	}
	return data, true
}	

func looking_for_improved_info(data_base map[string]interface{}) (string, map[string]interface{}) {	data_base, err := read_file(file_name)
	if !err {
		fmt.Println("السبب للخطأ هو:", err)
		return "", nil
	}

for key, value := range data_base {	
		user_map, ok := value.(map[string]interface{})
        if !ok {
            continue
		}
		start_value, has_start := user_map["start"]
        end_value, has_end := user_map["end"]
		if has_start && has_end && start_value == "start" && end_value == "end" {
            return key, user_map 
        }
	}
    return "", nil
}

func getFromList(m map[string]interface{}, key string, index int) string {
	data, ok := m[key]
	if !ok {
		return "" 
	}

	list, ok := data.([]interface{})
	if !ok || index < 0 || index >= len(list) {
		return "" 
	}

	val, ok := list[index].(string)
	if !ok {
		return "" 
	}

	return val
}

func getexercises(user_data map[string]interface{}, day int8) (per_day_exercises_sections []string,per_day_exercises_movement []string, per_day_exercises_sets []string) {
	per_day_exercises_sections = []string{""}
	per_day_exercises_movement = []string{""}
	per_day_exercises_sets = []string{""}
	string_day := fmt.Sprintf("%d", day)
	

	if list, ok := user_data["day"+string_day].([]interface{}); ok {
		if list[0].(string) == "استراحه" {
			per_day_exercises_sections = []string{"استراحه", "", "", "", "", "", "", ""}
			per_day_exercises_movement = []string{"استراحه", "", "", "", "", "", "", ""}
			per_day_exercises_sets = []string{"استراحه", "", "", "", "", "", "", ""}
			return per_day_exercises_sections, per_day_exercises_movement, per_day_exercises_sets
		}
	}

		i:= 0
		for  i < 7 {
			i+=1
			string_i := fmt.Sprintf("%d", i)
			per_day_exercises_sections = append(per_day_exercises_sections, getFromList(user_data["day"+string_day].(map[string]interface{}), "day"+string_day+"_exercise"+string_i, 0))
			per_day_exercises_movement = append(per_day_exercises_movement, getFromList(user_data["day"+string_day].(map[string]interface{}), "day"+string_day+"_exercise"+string_i, 1))
			per_day_exercises_sets = append(per_day_exercises_sets, getFromList(user_data["day"+string_day].(map[string]interface{}), "day"+string_day+"_exercise"+string_i, 2))

			if i == 7 {
				break
			}
		}
		return per_day_exercises_sections, per_day_exercises_movement, per_day_exercises_sets

}	
	
func delete_user_from_scheduler(data_base map[string]interface{}, user_id_in_scheduler string) bool { 
	delete(data_base, user_id_in_scheduler)
	file_data, err := json.MarshalIndent(data_base, "", "    ")
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return false
	}
	err = os.WriteFile(file_name, file_data, 0644)
	if err != nil {
		fmt.Println("Error writing file:", err)
		return false
	}
	return true
}

func write_in_file(user_id_in_scheduler string, user_data map[string]interface{}, user_id string, time_now string, user_name string, day int8, slide int8) bool {
    font_color := color.RGBA{0, 0, 0, 255}
    slide_string := fmt.Sprintf("%d", slide)
    _, movement, sets := getexercises(user_data, int8(day))
    _, movement2, sets2 := getexercises(user_data, int8(day+1))
    font_path := filepath.Join(main_path, "font", "22016-adobearabic.ttf") 
    
    if day == 1 || day == 2 {
        image_path = filepath.Join(main_path, "images", "Slide1.PNG")
    }
    if day == 3 || day == 4 {
        image_path = filepath.Join(main_path, "images", "Slide2.PNG")
    }
    if day == 5 || day == 6 {
        image_path = filepath.Join(main_path, "images", "Slide3.PNG")
    }
    
    image_file, err := os.Open(image_path)
    if err != nil {
        fmt.Println("Error opening image:", err)
        return false
    }
    defer image_file.Close()

    img, _, err := image.Decode(image_file)
    if err != nil {
        fmt.Println("Error decoding image:", err)
        return false
    }
    editableImg := image.NewRGBA(img.Bounds())
    draw.Draw(editableImg, img.Bounds(), img, image.Point{}, draw.Src)

    fontBytes, err := os.ReadFile(font_path)
    if err != nil {
        fmt.Println("Error reading font file:", err)
        return false
    }
    f, err := opentype.Parse(fontBytes)
    if err != nil {
        fmt.Println("Error parsing font file:", err)
        return false
    }
    face, err := opentype.NewFace(f, &opentype.FaceOptions{
        Size: 24, 
        DPI:  96,
    })
    if err != nil {
        fmt.Println("Error creating font face:", err)
        return false
    }   
    drawer := &font.Drawer{
        Dst:  editableImg,
        Src:  image.NewUniform(font_color),
        Face: face,
    }

    if movement[0] == "استراحه" {
        exercise1_day0_box := TextPosition{X:517 , Y:247 }
        txtRest := goarabic.Reverse(goarabic.ToGlyph("هذا اليوم استراحة"))
        drawer.Dot = fixed.P(exercise1_day0_box.X - drawer.MeasureString(txtRest).Round(), exercise1_day0_box.Y)
        drawer.DrawString(txtRest)
    }
    if movement2[0] == "استراحه" {
        exercise1_day1_box := TextPosition{X:517 , Y:616 }
        txtRest2 := goarabic.Reverse(goarabic.ToGlyph("هذا اليوم استراحة"))
        drawer.Dot = fixed.P(exercise1_day1_box.X - drawer.MeasureString(txtRest2).Round(), exercise1_day1_box.Y)
        drawer.DrawString(txtRest2)
    }
    
    name_box := TextPosition{X: 680, Y: 165}
    date_box := TextPosition{X: 150, Y: 165}

    txtName := goarabic.Reverse(goarabic.ToGlyph(user_name))
    drawer.Dot = fixed.P(name_box.X-drawer.MeasureString(txtName).Round(), name_box.Y)
    drawer.DrawString(txtName)

    txtDate := time_now
    drawer.Dot = fixed.P(date_box.X-drawer.MeasureString(txtDate).Round(), date_box.Y)
    drawer.DrawString(txtDate)

    if movement[0] != "استراحه" {
        box1 := TextPosition{X: 517, Y: 242}
        box2 := TextPosition{X: 517, Y: 287}
        box3 := TextPosition{X: 517, Y: 332}
        box4 := TextPosition{X: 517, Y: 377}
        box5 := TextPosition{X: 517, Y: 422}
        box6 := TextPosition{X: 517, Y: 467}
        box7 := TextPosition{X: 517, Y: 512}

        if movement[1] != "" {
            t := sets[1]+" "+goarabic.Reverse(goarabic.ToGlyph(movement[1] + " التعدادات:")) 
            drawer.Dot = fixed.P(box1.X-drawer.MeasureString(t).Round(), box1.Y)
            drawer.DrawString(t)
        }
        if movement[2] != "" {
            t := sets[2]+" "+goarabic.Reverse(goarabic.ToGlyph(movement[2] + " التعدادات:")) 
            drawer.Dot = fixed.P(box2.X-drawer.MeasureString(t).Round(), box2.Y)
            drawer.DrawString(t)
        }
        if movement[3] != "" {
            t := sets[3]+" "+goarabic.Reverse(goarabic.ToGlyph(movement[3] + " التعدادات:")) 
            drawer.Dot = fixed.P(box3.X-drawer.MeasureString(t).Round(), box3.Y)
            drawer.DrawString(t)
        }
        if movement[4] != "" {
            t := sets[4]+" "+goarabic.Reverse(goarabic.ToGlyph(movement[4] + " التعدادات:")) 
            drawer.Dot = fixed.P(box4.X-drawer.MeasureString(t).Round(), box4.Y)
            drawer.DrawString(t)
        }
        if movement[5] != "" {
            t := sets[5]+" "+goarabic.Reverse(goarabic.ToGlyph(movement[5] + " التعدادات:")) 
            drawer.Dot = fixed.P(box5.X-drawer.MeasureString(t).Round(), box5.Y)
            drawer.DrawString(t)
        }
        if movement[6] != "" {
            t := sets[6]+" "+goarabic.Reverse(goarabic.ToGlyph(movement[6] + " التعدادات:")) 
            drawer.Dot = fixed.P(box6.X-drawer.MeasureString(t).Round(), box6.Y)
            drawer.DrawString(t)
        }
        if movement[7] != "" {
            t := sets[7]+" "+goarabic.Reverse(goarabic.ToGlyph(movement[7] + " التعدادات:")) 
            drawer.Dot = fixed.P(box7.X-drawer.MeasureString(t).Round(), box7.Y)
            drawer.DrawString(t)
        }
    }

    // طباعة تمارين الجزء السفلي (اليوم التالي)
    if movement2[0] != "استراحه" {
        box1 := TextPosition{X: 517, Y: 611}
        box2 := TextPosition{X: 517, Y: 656}
        box3 := TextPosition{X: 517, Y: 701}
        box4 := TextPosition{X: 517, Y: 746}
        box5 := TextPosition{X: 517, Y: 791}
        box6 := TextPosition{X: 517, Y: 836}
        box7 := TextPosition{X: 517, Y: 881}

        if movement2[1] != "" {
            t := sets2[1]+" "+goarabic.Reverse(goarabic.ToGlyph(movement2[1] + " التعدادات:")) 
            drawer.Dot = fixed.P(box1.X-drawer.MeasureString(t).Round(), box1.Y)
            drawer.DrawString(t)
        }
        if movement2[2] != "" {
            t := sets2[2]+" "+goarabic.Reverse(goarabic.ToGlyph(movement2[2] + " التعدادات:")) 
            drawer.Dot = fixed.P(box2.X-drawer.MeasureString(t).Round(), box2.Y)
            drawer.DrawString(t)
        }
        if movement2[3] != "" {
            t := sets2[3]+" "+goarabic.Reverse(goarabic.ToGlyph(movement2[3] + " التعدادات:")) 
            drawer.Dot = fixed.P(box3.X-drawer.MeasureString(t).Round(), box3.Y)
            drawer.DrawString(t)
        }
        if movement2[4] != "" {
            t := sets2[4]+" "+goarabic.Reverse(goarabic.ToGlyph(movement2[4] + " التعدادات:")) 
            drawer.Dot = fixed.P(box4.X-drawer.MeasureString(t).Round(), box4.Y)
            drawer.DrawString(t)
        }
        if movement2[5] != "" {
            t := sets2[5]+" "+goarabic.Reverse(goarabic.ToGlyph(movement2[5] + " التعدادات:")) 
            drawer.Dot = fixed.P(box5.X-drawer.MeasureString(t).Round(), box5.Y)
            drawer.DrawString(t)
        }
        if movement2[6] != "" {
            t := sets2[6]+" "+goarabic.Reverse(goarabic.ToGlyph(movement2[6] + " التعدادات:")) 
            drawer.Dot = fixed.P(box6.X-drawer.MeasureString(t).Round(), box6.Y)
            drawer.DrawString(t)
        }
        if movement2[7] != "" {
            t := sets2[7]+" "+goarabic.Reverse(goarabic.ToGlyph(movement2[7] + " التعدادات:")) 
            drawer.Dot = fixed.P(box7.X-drawer.MeasureString(t).Round(), box7.Y)
            drawer.DrawString(t)
        }
    }

    tempfile := filepath.Join(main_path, "tempimage", user_id)
    os.MkdirAll(tempfile, 0755)
    finalFileName := filepath.Join(tempfile,  "slide"+ slide_string +".png")
    out, _ := os.Create(finalFileName)
    png.Encode(out, editableImg)
    out.Close()

    allimages := filepath.Join(main_path, "allimages" , user_id_in_scheduler)
    os.MkdirAll(allimages, 0755)
    finalAllimages := filepath.Join(allimages, "slide"+ slide_string +".png")
    out, _ = os.Create(finalAllimages)
    png.Encode(out, editableImg)
    out.Close()

    return true
}

	



// main function
func main() {
	for {
		if !is_file_exist(file_name) {
			fmt.Println("File does not exist. Please create the file and try again.")
			time.Sleep(5 * time.Second)
			continue
		}
		data_base, error := read_file(file_name)
		if !error {
			fmt.Println("Error reading file.")
			time.Sleep(5 * time.Second)
			continue
		}

		user_id_in_scheduler, user_data := looking_for_improved_info(data_base)
		if user_data == nil && user_id_in_scheduler == "" {
			time.Sleep(2 * time.Second)
			fmt.Println("No user found with start and end values. Retrying...")
			continue
		}
		user_id := user_data["user_id"].(string)
		user_name := user_data["name"].(string)
		time_now := time.Now().Format("02/01/2006")
		var slide int8 = 1
		var day int8 = 1
		for {
			write_in_file(user_id_in_scheduler,user_data,user_id,time_now,user_name, day , slide) 
			day = day + 2
			slide += 1
			if day >= 6	{
				break
			}		
				
		}
		delete_user_from_scheduler(data_base, user_id_in_scheduler)



		
		
			
			
		}
	}



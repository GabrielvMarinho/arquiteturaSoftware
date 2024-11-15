package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController //api rest spring
public class DemoController {


    @GetMapping("/iotDataGet")
    public Integer getData(){
        return (int) (Math.random()*100);
    }
}

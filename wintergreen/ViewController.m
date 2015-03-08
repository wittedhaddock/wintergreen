//
//  ViewController.m
//  wintergreen
//
//  Created by James Graham on 3/8/15.
//  Copyright (c) 2015 JamesGraham. All rights reserved.
//

#import "ViewController.h"
#import <CoreMotion/CoreMotion.h>

@interface ViewController ()
@property (strong, nonatomic) CMMotionManager *manager;

//gyro
@property (weak, nonatomic) IBOutlet UILabel *gX;
@property (weak, nonatomic) IBOutlet UILabel *gY;
@property (weak, nonatomic) IBOutlet UILabel *gZ;

//accel
@property (weak, nonatomic) IBOutlet UILabel *aX;
@property (weak, nonatomic) IBOutlet UILabel *aY;
@property (weak, nonatomic) IBOutlet UILabel *aZ;

@end

@implementation ViewController

- (CMMotionManager *)manager{
    if(!_manager){
        _manager = [[CMMotionManager alloc] init];
    }
    return _manager;
}

- (void)viewDidLoad {
    [super viewDidLoad];

    if ([self.manager isGyroAvailable] && [self.manager isGyroActive] == NO) {
        [self startGryoUpdate];
    }
}

- (void)startGryoUpdate{
    [self.manager setGyroUpdateInterval:0.01f];
    [self.manager startGyroUpdatesToQueue:[NSOperationQueue mainQueue]
                              withHandler:^(CMGyroData *gyroData, NSError *error) {
                                  if (!error) {
                                      [self processGyroData:gyroData];
                                  }
                                  else {
                                      NSLog(@"ERROR:\n%@", [error userInfo]);
                                  }
                              }];
}
- (void)processGyroData:(CMGyroData *)data{
    double x = data.rotationRate.x;
    double y = data.rotationRate.y;
    double z = data.rotationRate.z;
    [self updateViewWithNewGyroDataX:x Y:y Z:z];
}

- (void)updateViewWithNewGyroDataX:(double)x Y:(double)y Z:(double)z{
    self.gX.text = [NSString stringWithFormat:@"X: %f", x];
    self.gY.text = [NSString stringWithFormat:@"Y: %f", y];
    self.gZ.text = [NSString stringWithFormat:@"Z: %f", z];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
